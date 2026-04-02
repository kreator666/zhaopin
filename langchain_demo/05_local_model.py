"""
本地模型运行示例
使用 Ollama 运行开源大模型，无需 API Key，完全免费
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def check_ollama():
    """检查 Ollama 是否安装"""
    import subprocess
    import sys
    
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama 已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Ollama 未安装")
    print("   1. 访问 https://ollama.com 下载安装")
    print("   2. 安装后运行: ollama pull qwen2.5:7b")
    return False


def local_model_example():
    """本地模型示例"""
    # 使用 Ollama 加载本地模型
    # 需要先运行: ollama pull qwen2.5:7b
    llm = Ollama(model="qwen2.5:7b")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位专业助手。"),
        ("human", "{question}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    print("=== 本地模型问答 ===\n")
    questions = [
        "什么是人工智能？",
        "用 Python 写个 Hello World",
    ]
    
    for q in questions:
        print(f"❓ {q}")
        print(f"💡 {chain.invoke({'question': q})}")
        print()


def local_embedding_example():
    """本地嵌入模型示例 - 实现完全本地的 RAG"""
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_text_splitters import CharacterTextSplitter
    
    # 文档
    text = """LangChain 是一个用于开发 LLM 应用的框架。
    它提供了链式调用、记忆、工具使用等组件。
    RAG 是检索增强生成的缩写，结合了检索和生成。"""
    
    # 分割
    splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split_text(text)
    
    # 本地嵌入模型
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # 创建向量库
    vectorstore = Chroma.from_texts(chunks, embeddings)
    
    # 检索
    retriever = vectorstore.as_retriever(k=1)
    docs = retriever.invoke("什么是 RAG？")
    
    print("=== 本地 RAG 检索 ===")
    print(f"查询: 什么是 RAG？")
    print(f"检索结果: {docs[0].page_content}\n")
    
    # 使用本地 LLM 回答
    llm = Ollama(model="qwen2.5:7b")
    response = llm.invoke(f"基于以下信息回答问题：{docs[0].page_content}\n\n问题：什么是RAG？")
    print(f"回答: {response}")


if __name__ == "__main__":
    print("🚀 本地模型示例 (Ollama)\n")
    
    if not check_ollama():
        exit(1)
    
    # 检查模型是否下载
    import subprocess
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "qwen2.5" not in result.stdout:
        print("\n📥 请先下载模型:")
        print("   ollama pull qwen2.5:7b")
        print("   ollama pull nomic-embed-text")
        exit(1)
    
    local_model_example()
    print()
    local_embedding_example()
    
    print("\n✅ 本地模型运行完成！")

"""
Moonshot (Kimi) 大模型示例
Kimi 是月之暗面推出的中文大模型，支持超长上下文
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def kimi_basic_chat():
    """Kimi 基础对话"""
    # Kimi 兼容 OpenAI API 格式
    llm = ChatOpenAI(
        model="moonshot-v1-8k",  # 可选: moonshot-v1-8k/32k/128k
        temperature=0.7,
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是 Kimi，由月之暗面开发的人工智能助手。"),
        ("human", "{question}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    print("=== Kimi 基础对话 ===\n")
    questions = [
        "你好，请介绍一下你自己",
        "用三句话解释什么是量子计算",
    ]
    
    for q in questions:
        print(f"[Q] {q}")
        print(f"[A] {chain.invoke({'question': q})}\n")


def kimi_with_context():
    """Kimi 长文本处理示例 - 利用 Kimi 的长上下文优势"""
    llm = ChatOpenAI(
        model="moonshot-v1-128k",  # 使用 128k 长上下文模型
        temperature=0.3,
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    
    # 模拟一篇长文章
    long_article = """
    [此处省略一篇很长的文章...]
    人工智能（Artificial Intelligence），英文缩写为AI。
    它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。
    
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    
    人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，
    将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。
    
    人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    
    人工智能是一门极富挑战性的科学，从事这项工作的人必须懂得计算机知识，心理学和哲学。
    人工智能是包括十分广泛的科学，它由不同的领域组成，如机器学习，计算机视觉等等，
    总的说来，人工智能研究的一个主要目标是使机器能够胜任一些通常需要人类智能才能完成的复杂工作。
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位专业的文章分析助手。请基于提供的文章内容回答问题。"),
        ("human", "文章内容：\n{article}\n\n问题：{question}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    print("=== Kimi 长文本分析 ===\n")
    result = chain.invoke({
        "article": long_article,
        "question": "总结这篇文章的主要内容"
    })
    print(f"[A] {result}\n")


def kimi_streaming():
    """Kimi 流式输出"""
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        streaming=True,
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    
    print("=== Kimi 流式输出 ===\n")
    print("[Q] 请写一个Python快速排序\n")
    print("[A] ", end="", flush=True)
    
    for chunk in llm.stream("请写一个Python快速排序算法，并添加注释"):
        print(chunk.content, end="", flush=True)
    
    print("\n")


def kimi_rag_example():
    """Kimi + RAG 示例"""
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_text_splitters import CharacterTextSplitter
    
    # 注意：Kimi 不提供嵌入模型，我们使用 OpenAI 或其他嵌入模型
    # 如果使用本地嵌入，可以改用 OllamaEmbeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 或者使用本地嵌入（需要 ollama）
    # from langchain_community.embeddings import OllamaEmbeddings
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # 示例文档
    documents = [
        "Kimi 是由月之暗面科技有限公司开发的人工智能助手。",
        "Kimi 支持超长上下文窗口，最高可达 200 万字。",
        "Kimi 擅长中文对话、文档分析和代码编写。",
    ]
    
    # 创建向量库
    vectorstore = Chroma.from_texts(documents, embeddings)
    retriever = vectorstore.as_retriever(k=2)
    
    # 检索相关文档
    question = "Kimi 有什么特点？"
    docs = retriever.invoke(question)
    
    # 使用 Kimi 生成回答
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    
    context = "\n".join([d.page_content for d in docs])
    prompt = f"基于以下信息回答问题：\n\n{context}\n\n问题：{question}"
    
    print("=== Kimi + RAG 示例 ===\n")
    print(f"[Q] {question}")
    print(f"[A] {llm.invoke(prompt).content}\n")


if __name__ == "__main__":
    print("[Kimi] Moonshot 示例\n")
    
    if not os.getenv("MOONSHOT_API_KEY"):
        print("[!] 请先设置 MOONSHOT_API_KEY 环境变量")
        print("   获取方式：")
        print("   1. 访问 https://platform.moonshot.cn")
        print("   2. 注册账号并创建 API Key")
        print("   3. 复制 .env.example 为 .env")
        print("   4. 在 .env 文件中填写 MOONSHOT_API_KEY=你的密钥")
        exit(1)
    
    kimi_basic_chat()
    kimi_with_context()
    kimi_streaming()
    
    # 如果有 OpenAI Key 或本地嵌入模型，可以运行 RAG 示例
    if os.getenv("OPENAI_API_KEY") or os.getenv("LOCAL_EMBEDDING"):
        kimi_rag_example()
    else:
        print("[i] 跳过 RAG 示例（需要嵌入模型）")
    
    print("[OK] Kimi 示例执行完成！")

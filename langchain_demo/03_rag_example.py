"""
RAG (检索增强生成) 示例
演示如何结合文档检索和 LLM 生成来回答问题
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def load_documents():
    """加载文档并分割"""
    # 读取示例文本
    with open("data/sample_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # 文本分割器
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=200,
        chunk_overlap=50,
    )
    
    # 分割文档
    chunks = text_splitter.split_text(text)
    print(f"📄 文档已分割为 {len(chunks)} 个片段")
    return chunks


def create_vector_store(chunks):
    """创建向量数据库"""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 使用 Chroma 作为向量存储（内存模式）
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name="demo_collection",
    )
    print("✅ 向量数据库创建完成")
    return vectorstore


def create_rag_chain(vectorstore):
    """创建 RAG Chain"""
    # 检索器
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}  # 返回最相关的 2 个片段
    )
    
    # Prompt 模板
    template = """基于以下上下文回答问题。如果上下文不包含答案，请说"根据提供的信息无法回答"。

上下文：
{context}

问题：{question}

请用中文回答："""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 格式化文档的函数
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # 构建 RAG Chain
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def main():
    print("🚀 RAG 检索增强生成示例\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请先设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    # 1. 加载文档
    chunks = load_documents()
    
    # 2. 创建向量数据库
    vectorstore = create_vector_store(chunks)
    
    # 3. 创建 RAG Chain
    rag_chain = create_rag_chain(vectorstore)
    
    # 4. 测试问题
    questions = [
        "什么是 LangChain？",
        "深度学习是什么的子集？",
        "量子计算有什么应用？",  # 文档中未提及
    ]
    
    print("\n=== 问答测试 ===\n")
    for question in questions:
        print(f"❓ 问题: {question}")
        answer = rag_chain.invoke(question)
        print(f"💡 回答: {answer}")
        print()


if __name__ == "__main__":
    main()

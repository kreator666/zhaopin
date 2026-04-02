"""
DeepSeek 大模型示例
DeepSeek 价格便宜，新用户有 5000 万 Tokens 免费额度
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def deepseek_chat():
    """DeepSeek 对话示例"""
    llm = ChatOpenAI(
        model="deepseek-chat",  # 或 deepseek-reasoner（推理模型）
        temperature=0.7,
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是 DeepSeek，一个 helpful 的 AI 助手。"),
        ("human", "{question}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    print("=== DeepSeek Chat ===\n")
    
    questions = [
        "你好，请介绍一下你自己",
        "用一句话解释神经网络",
    ]
    
    for q in questions:
        print(f"[Q] {q}")
        print(f"[A] {chain.invoke({'question': q})}\n")


def deepseek_reasoning():
    """DeepSeek 推理模型示例（适合数学/逻辑）"""
    llm = ChatOpenAI(
        model="deepseek-reasoner",  # 推理模型
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )
    
    print("=== DeepSeek Reasoning ===\n")
    
    question = "一个水池有进水管和出水管，单开进水管5小时注满，单开出水管7小时排空。同时开两个管，几小时注满？"
    
    print(f"[Q] {question}\n")
    response = llm.invoke(question)
    print(f"[A] {response.content}\n")


if __name__ == "__main__":
    print("[DeepSeek] Example\n")
    
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("[!] Please set DEEPSEEK_API_KEY")
        print("   1. Visit https://platform.deepseek.com")
        print("   2. Register and create API Key")
        print("   3. Add DEEPSEEK_API_KEY to .env file")
        exit(1)
    
    deepseek_chat()
    deepseek_reasoning()
    
    print("[OK] DeepSeek example completed!")

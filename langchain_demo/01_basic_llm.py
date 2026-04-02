"""
基础 LLM 调用示例
演示如何使用 LangChain 调用 OpenAI 模型
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 加载环境变量
load_dotenv()


def basic_chat():
    """基础对话示例"""
    # 初始化模型
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 方式 1: 直接调用
    response = llm.invoke("请用一句话介绍 LangChain")
    print("=== 方式 1: 直接调用 ===")
    print(response.content)
    print()
    
    # 方式 2: 使用消息列表
    messages = [
        SystemMessage(content="你是一位专业的 AI 助手，回答要简洁明了。"),
        HumanMessage(content="什么是机器学习？"),
    ]
    response = llm.invoke(messages)
    print("=== 方式 2: 使用消息列表 ===")
    print(response.content)
    print()
    
    # 方式 3: 批量调用
    questions = [
        "Python 是什么？",
        "深度学习有什么应用？",
    ]
    responses = llm.batch(questions)
    print("=== 方式 3: 批量调用 ===")
    for q, r in zip(questions, responses):
        print(f"Q: {q}")
        print(f"A: {r.content}")
        print()


def streaming_chat():
    """流式输出示例"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        streaming=True,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    print("=== 流式输出示例 ===")
    for chunk in llm.stream("讲一个关于程序员的短笑话"):
        print(chunk.content, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    print("🚀 LangChain 基础 LLM 调用示例\n")
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请先设置 OPENAI_API_KEY 环境变量")
        print("   复制 .env.example 为 .env 并填写你的 API Key")
        exit(1)
    
    basic_chat()
    streaming_chat()
    
    print("✅ 示例执行完成！")

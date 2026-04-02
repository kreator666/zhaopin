"""
简单 Chain 示例
演示如何使用 PromptTemplate + LLM + OutputParser 构建 Chain
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()


def simple_chain():
    """简单的 Prompt -> LLM -> Parser Chain"""
    # 定义 Prompt 模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位{role}，请用{style}风格回答问题。"),
        ("human", "{question}"),
    ])
    
    # 初始化模型
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 输出解析器
    output_parser = StrOutputParser()
    
    # 构建 Chain: prompt | llm | parser
    chain = prompt | llm | output_parser
    
    # 调用 Chain
    result = chain.invoke({
        "role": "技术专家",
        "style": "通俗易懂",
        "question": "什么是 API？"
    })
    
    print("=== 简单 Chain 示例 ===")
    print(result)
    print()


def chain_with_transform():
    """带数据转换的 Chain"""
    # 翻译 Chain
    prompt = ChatPromptTemplate.from_template(
        "将以下中文翻译成英文：\n\n{chinese_text}"
    )
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 添加自定义转换步骤
    def add_prefix(output: str) -> str:
        return f"【翻译结果】\n{output}"
    
    chain = prompt | llm | StrOutputParser() | RunnableLambda(add_prefix)
    
    result = chain.invoke({"chinese_text": "人工智能正在改变世界。"})
    print("=== 带转换的 Chain 示例 ===")
    print(result)
    print()


def batch_processing():
    """批量处理示例"""
    prompt = ChatPromptTemplate.from_template(
        "用一句话总结以下主题：{topic}"
    )
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    chain = prompt | llm | StrOutputParser()
    
    topics = [
        {"topic": "区块链"},
        {"topic": "元宇宙"},
        {"topic": "量子计算"},
    ]
    
    results = chain.batch(topics)
    
    print("=== 批量处理示例 ===")
    for t, r in zip(topics, results):
        print(f"{t['topic']}: {r}")
    print()


if __name__ == "__main__":
    print("🚀 LangChain Chain 示例\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请先设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    simple_chain()
    chain_with_transform()
    batch_processing()
    
    print("✅ 示例执行完成！")

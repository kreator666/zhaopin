"""
Agent 示例
演示如何使用工具调用 Agent 来执行复杂任务
"""

import os
import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


# 定义工具
@tool
def search_weather(city: str) -> str:
    """查询指定城市的天气"""
    # 模拟天气查询
    weathers = ["晴天", "多云", "阴天", "小雨", "大雨"]
    temperatures = range(15, 35)
    weather = random.choice(weathers)
    temp = random.choice(temperatures)
    return f"{city}今天{weather}，气温{temp}°C"


@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("当前时间是 %Y年%m月%d日 %H:%M:%S")


def simple_agent_example():
    """简单 Agent 示例"""
    print("=== 简单 Agent 示例 ===\n")
    
    # 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    # 创建工具列表
    tools = [search_weather, calculate, get_current_time]
    
    # 创建 ReAct Agent
    agent = create_react_agent(llm, tools)
    
    # 测试查询
    queries = [
        "北京今天天气怎么样？",
        "23乘以47等于多少？",
        "现在几点了？",
    ]
    
    for query in queries:
        print(f"🤔 用户: {query}")
        response = agent.invoke({"messages": [("human", query)]})
        ai_message = response["messages"][-1]
        print(f"🤖 AI: {ai_message.content}\n")


def multi_step_agent_example():
    """多步骤 Agent 示例"""
    print("=== 多步骤 Agent 示例 ===\n")
    
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    
    tools = [search_weather, calculate, get_current_time]
    agent = create_react_agent(llm, tools)
    
    # 需要多步思考的查询
    query = "如果上海今天气温是25度，比北京高多少度？（先查两地的天气）"
    
    print(f"🤔 用户: {query}")
    response = agent.invoke({"messages": [("human", query)]})
    
    # 打印思考过程
    print("\n📋 思考过程:")
    for msg in response["messages"]:
        if msg.type == "ai":
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"  🤖 思考: 我需要调用工具")
                for tc in msg.tool_calls:
                    print(f"     工具: {tc['name']}, 参数: {tc['args']}")
            else:
                print(f"  🤖 回答: {msg.content}")
        elif msg.type == "tool":
            print(f"  🔧 工具返回: {msg.content}")
    
    print()


if __name__ == "__main__":
    print("🚀 LangChain Agent 示例\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  请先设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    simple_agent_example()
    multi_step_agent_example()
    
    print("✅ 示例执行完成！")

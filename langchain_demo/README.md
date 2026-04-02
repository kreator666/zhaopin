# LangChain 示例项目

这是一个完整的 LangChain 示例项目，展示了 LangChain 的核心功能和用法。

## 📁 项目结构

```
langchain_demo/
├── .env.example           # 环境变量配置示例
├── requirements.txt       # 项目依赖
├── README.md              # 本文件
├── 01_basic_llm.py        # 基础 LLM 调用示例
├── 02_simple_chain.py     # Chain 构建示例
├── 03_rag_example.py      # RAG 检索增强生成示例
├── 04_agent_example.py    # Agent 工具调用示例
├── 05_local_model.py      # 本地模型 (Ollama) 示例
├── 06_kimi_example.py     # Moonshot (Kimi) 示例
└── data/
    └── sample_text.txt    # RAG 示例用的文档
```

## 🚀 快速开始

### 1. 配置环境

复制环境变量示例文件并填写你的 API Key：

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

编辑 `.env` 文件，填入你的 OpenAI API Key：

```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1  # 如有需要可修改
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行示例

```bash
# 基础 LLM 调用
python 01_basic_llm.py

# Chain 构建
python 02_simple_chain.py

# RAG 检索增强
python 03_rag_example.py

# Agent 工具调用
python 04_agent_example.py

# 本地模型 (Ollama)
python 05_local_model.py

# Moonshot (Kimi)
python 06_kimi_example.py
```

## 📖 示例说明

### 01_basic_llm.py - 基础 LLM 调用

展示如何使用 LangChain 调用 OpenAI 模型：

- ✅ 直接调用
- ✅ 使用消息列表 (System/Human Message)
- ✅ 批量调用
- ✅ 流式输出

### 02_simple_chain.py - Chain 构建

展示如何构建处理流程 Chain：

- ✅ PromptTemplate + LLM + OutputParser
- ✅ 带自定义转换的 Chain
- ✅ 批量处理

### 03_rag_example.py - RAG 检索增强

展示如何实现检索增强生成：

- ✅ 文档加载和分割
- ✅ 向量数据库 (Chroma)
- ✅ 相似度检索
- ✅ 结合检索结果的生成

### 04_agent_example.py - Agent 工具调用

展示如何让 LLM 使用工具：

- ✅ 自定义工具定义
- ✅ ReAct Agent
- ✅ 多步骤推理

### 05_local_model.py - 本地模型 (Ollama)

展示如何使用本地开源模型：

- ✅ Ollama 本地模型调用
- ✅ 本地嵌入模型
- ✅ 完全离线的 RAG

### 06_kimi_example.py - Moonshot (Kimi)

展示如何使用 Kimi 大模型：

- ✅ Kimi 基础对话
- ✅ 长文本处理（128k 上下文）
- ✅ 流式输出
- ✅ Kimi + RAG

## 🔑 核心概念

| 概念 | 说明 |
|------|------|
| **Model** | 语言模型，如 GPT-4、Kimi、Llama |
| **Prompt** | 提示词模板，定义输入格式 |
| **Chain** | 处理流程链，串联多个组件 |
| **Retriever** | 检索器，从向量库查找相关文档 |
| **Agent** | 智能体，可自主决策使用工具 |
| **Memory** | 记忆组件，保存对话历史 |

## 📝 自定义扩展

### 添加新工具

在 `04_agent_example.py` 中，你可以添加更多工具：

```python
@tool
def my_tool(param: str) -> str:
    """工具描述（LLM 根据这个描述决定何时使用）"""
    # 工具逻辑
    return result
```

### 添加新数据源

在 `03_rag_example.py` 中，可以加载更多文档：

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("data/your_file.txt")
documents = loader.load()
```

## 🔗 相关资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain API 参考](https://api.python.langchain.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)

## 🌐 模型配置指南

### OpenAI

```
OPENAI_API_KEY=sk-your-key
OPENAI_API_BASE=https://api.openai.com/v1
```

### Moonshot (Kimi) ⭐推荐

国内可直接访问，新用户有免费额度：

1. 访问 https://platform.moonshot.cn 注册
2. 创建 API Key
3. 配置环境变量：

```
MOONSHOT_API_KEY=your-moonshot-key
```

可用模型：`moonshot-v1-8k` / `moonshot-v1-32k` / `moonshot-v1-128k`

### DeepSeek

1. 访问 https://platform.deepseek.com 注册
2. 配置环境变量：

```
DEEPSEEK_API_KEY=your-deepseek-key
```

### 本地模型 (Ollama)

无需 API Key，完全免费：

1. 安装 Ollama：https://ollama.com
2. 下载模型：
   ```bash
   ollama pull qwen2.5:7b    # 中文较好
   ollama pull llama3.2       # 英文较好
   ollama pull nomic-embed-text  # 嵌入模型
   ```

## 💡 常见问题

### 1. API Key 错误

确保 `.env` 文件配置正确，并已加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. 模型访问限制

某些地区可能需要使用代理或第三方 API：

```
OPENAI_API_BASE=https://your-proxy-url.com/v1
```

### 3. Chroma 内存警告

RAG 示例使用内存模式，程序结束后数据会消失。如需持久化，修改：

```python
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 添加持久化目录
)
```

---

🎉 祝你学习愉快！

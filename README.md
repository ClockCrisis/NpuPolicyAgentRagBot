# 智扫通机器人智能客服

基于 Streamlit 和 LangChain 的扫地机器人智能客服系统，支持 RAG 知识库问答和个人使用报告生成。

## 环境要求

- Python 3.10+
- Streamlit
- LangChain
- Chroma (向量数据库)
- 阿里云 DashScope API (通义千问模型)

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository_url>
cd AgentP
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

如果没有 requirements.txt，请手动安装核心依赖：

```bash
pip install streamlit langchain langchain-community langchain-chroma langchain-text-splitters langgraph dashscope
```

### 4. 配置 API 密钥

系统使用阿里云 DashScope API，需要设置环境变量：

```bash
# Windows
set DASHSCOPE_API_KEY=your_api_key
# Linux/Mac
export DASHSCOPE_API_KEY=your_api_key
```

或在代码中配置（不推荐用于生产环境）。

### 5. 初始化知识库

首次运行前，需要将知识库文档加载到向量数据库：

```bash
python -m rag.vector_store
```

系统会自动：
- 扫描 `data/` 目录下的 PDF 和 TXT 文件
- 计算文件 MD5 去重
- 分块处理并存储到 Chroma 向量库

## 运行应用

```bash
streamlit run app.py
```

启动后访问 http://localhost:8501

## 功能说明

### 1. 智能问答
基于 RAG 知识库回答扫地机器人相关问题，包括：
- 故障排除
- 维护保养
- 选购指南
- 常见问题

### 2. 使用报告生成
输入"生成我的使用报告"或类似请求，系统会：
1. 获取用户 ID
2. 获取当前月份
3. 调用 `fill_context_for_report` 切换到报告提示词
4. 获取用户使用数据
5. 生成个性化报告

### 3. 动态提示词切换
- 普通问答：使用 `main_prompt.txt`
- 报告生成：自动切换到 `report_prompt.txt`

## 目录结构

```
AgentP/
├── app.py                    # Streamlit 应用入口
├── agent/                    # Agent 核心模块
│   ├── react_agent.py        # ReAct Agent 编排器
│   └── tools/
│       ├── agent_tools.py    # Agent 工具集
│       └── middleware.py      # 中间件
├── rag/                      # RAG 模块
│   ├── rag_service.py        # RAG 摘要服务
│   └── vector_store.py       # 向量存储
├── model/                    # 模型层
│   └── factory.py            # 模型工厂
├── config/                   # 配置文件
│   ├── agent.yml             # Agent 配置
│   ├── chroma.yml            # 向量库配置
│   └── prompts.yml           # 提示词路径配置
├── prompts/                  # 提示词模板
│   ├── main_prompt.txt
│   ├── rag_summarize.txt
│   └── report_prompt.txt
├── utils/                    # 工具模块
├── data/                     # 知识库文档
└── chroma_db/                # 向量数据库存储
```

## 配置说明

### agent.yml
```yaml
chat_model_name: qwen3-max
embedding_model_name: text-embedding-v4
```

### chroma.yml
```yaml
collection_name: agent
persist_directory: chroma_db
k: 3                    # 检索返回数量
data_path: data
chunk_size: 200
chunk_overlap: 20
```

## 扩展知识库

将 PDF 或 TXT 格式的文档放入 `data/` 目录，然后运行：

```bash
python -m rag.vector_store
```

系统会自动跳过已处理的文档（通过 MD5 验证）。

## 日志

日志文件位于 `logs/` 目录下。

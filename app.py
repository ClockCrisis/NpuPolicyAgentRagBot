import time
import os
import tempfile

import streamlit as st
from agent.react_agent import ReactAgent
from utils.config_handler import rag_conf
from rag.vector_store import VectorStoreService
from utils.path_tool import get_abs_path

# 打印模型配置信息
# def print_model_info():
#     provider = rag_conf.get("model_provider", "dashscope")
#     print("=" * 50)
#     print("模型配置信息")
#     print("=" * 50)
#     print(f"模型提供商: {provider}")
#     if provider == "openai":
#         openai_conf = rag_conf.get("openai", {})
#         print(f"聊天模型: {openai_conf.get('chat_model')}")
#         print(f"API 地址: {openai_conf.get('base_url')}")
#     else:
#         print(f"聊天模型: {rag_conf.get('chat_model_name')}")
#     print(f"嵌入模型: {rag_conf.get('embedding_model_name')}")
#     print("=" * 50)

# print_model_info()


def extract_text_from_file(file) -> str:
    """从 PDF/DOCX/TXT 文件提取文本"""
    suffix = file.name.lower().split('.')[-1]

    if suffix == 'txt':
        return file.getvalue().decode("utf-8")

    elif suffix == 'pdf':
        from langchain_community.document_loaders import PyPDFLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            return "\n\n".join(doc.page_content for doc in docs)
        finally:
            os.unlink(tmp_path)

    elif suffix == 'docx':
        from langchain_community.document_loaders import Docx2txtLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name
        try:
            loader = Docx2txtLoader(tmp_path)
            docs = loader.load()
            return "\n\n".join(doc.page_content for doc in docs)
        finally:
            os.unlink(tmp_path)

    else:
        raise ValueError(f"不支持的文件类型: {suffix}")


# 文件上传功能
def show_file_uploader():
    st.sidebar.divider()
    st.sidebar.subheader("上传知识库文件")

    uploaded_file = st.sidebar.file_uploader(
        "选择文件",
        type=["pdf", "docx", "txt"],
        help="支持 PDF、DOCX、TXT 格式"
    )

    if uploaded_file is not None:
        st.sidebar.write(f"**文件名:** {uploaded_file.name}")
        st.sidebar.write(f"**大小:** {uploaded_file.size / 1024:.1f} KB")

        if st.sidebar.button("上传并添加到知识库", type="primary"):
            try:
                # 提取文本
                text = extract_text_from_file(uploaded_file)

                if not text.strip():
                    st.sidebar.error("文件内容为空")
                else:
                    # 保存文件到 data 目录
                    data_path = get_abs_path("data")
                    file_path = os.path.join(data_path, uploaded_file.name)

                    # 如果文件已存在，先删除
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    # 保存文件
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    # 添加到向量库
                    vs_service = VectorStoreService()
                    success = vs_service.add_document(text, uploaded_file.name)

                    if success:
                        st.sidebar.success("文件上传并添加到知识库成功！")
                    else:
                        st.sidebar.error("添加到知识库失败")

            except Exception as e:
                st.sidebar.error(f"处理失败: {str(e)}")


st.title("智扫通机器人智能客服")
st.divider()

# 显示文件上传组件
show_file_uploader()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()

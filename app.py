import time

import streamlit as st
from agent.react_agent import ReactAgent
from utils.config_handler import rag_conf

# 打印模型配置信息
def print_model_info():
    provider = rag_conf.get("model_provider", "dashscope")
    print("=" * 50)
    print("模型配置信息")
    print("=" * 50)
    print(f"模型提供商: {provider}")
    if provider == "openai":
        openai_conf = rag_conf.get("openai", {})
        print(f"聊天模型: {openai_conf.get('chat_model')}")
        print(f"API 地址: {openai_conf.get('base_url')}")
    else:
        print(f"聊天模型: {rag_conf.get('chat_model_name')}")
    print(f"嵌入模型: {rag_conf.get('embedding_model_name')}")
    print("=" * 50)

print_model_info()

# 标题
st.title("智扫通机器人智能客服")
st.divider()

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

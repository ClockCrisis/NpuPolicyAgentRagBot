from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.config_handler import rag_conf


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        provider = rag_conf.get("model_provider", "dashscope")
        if provider == "openai":
            openai_conf = rag_conf.get("openai", {})
            return ChatOpenAI(
                model=openai_conf.get("chat_model", "gpt-4o"),
                base_url=openai_conf.get("base_url", "https://api.openai.com/v1"),
                api_key=openai_conf.get("api_key", ""),
            )
        return ChatTongyi(model=rag_conf["chat_model_name"])


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()

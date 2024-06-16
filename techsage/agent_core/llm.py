import os

from langchain_openai.chat_models import ChatOpenAI

params = {
    "model": os.environ["OPENAI_MODEL_NAME"],
}
if os.environ["LOCAL"] == "true":
    params["base_url"] = os.environ["OPENAI_API_BASE"]

llm = ChatOpenAI(**params)

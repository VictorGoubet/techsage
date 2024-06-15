import os

import openai
from langchain_openai.chat_models import ChatOpenAI

params = {
    "model": os.environ["OPENAI_MODEL_NAME"],
}
if os.environ["LOCAL"] == "true":
    params["base_url"] = os.environ["OPENAI_API_BASE"]
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]
    params["api_key"] = openai.api_key

llm = ChatOpenAI(**params)

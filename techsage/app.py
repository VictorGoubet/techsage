import os
import traceback
from typing import Callable, Union

import streamlit as st

from techsage.agent_core.crew import TechSageCrew
from techsage.configure import configure
from techsage.utils.constants import DEFAULT_CONFIG
from techsage.utils.load_config import load_config
from techsage.utils.tools import ansi_to_html


class TechSageChatApp:
    """TechSage Chat Application using Streamlit"""

    def __init__(self) -> None:
        """Initialize the app"""
        self._load_current_config()
        self._initialize_streamlit_ui()

    def _initialize_streamlit_ui(self) -> None:
        """Initialize the Streamlit user interface"""
        st.set_page_config(page_title="TechSage Chat", layout="wide")
        st.title("👋 Welcome to TechSage Information Gatherer")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        with st.sidebar:
            st.title("Settings")

            st.text_input("Model", key="model")
            st.text_input("Model URL", key="model_url")
            st.text_input("OpenAI API Key", key="openai_key")
            st.text_input("Google Search API Key", key="google_key")
            st.checkbox("Local", key="local")
            col1, col2 = st.columns(2)
            with col1:
                st.button("Save", on_click=self._save_config)
            with col2:
                st.button("Refresh", on_click=self._load_current_config)

        self._display_chat_history()
        if prompt := st.chat_input("Kubernetes.."):
            self._send_message(prompt)

    def _save_config(self) -> None:
        """Save the current configuration"""
        model = st.session_state["model"]
        model_url = st.session_state["model_url"]
        openai_key = st.session_state["openai_key"]
        google_key = st.session_state["google_key"]
        local = st.session_state["local"]
        try:
            configure(model, openai_key, google_key, local, 0, model_url)
            load_config()
        except Exception as e:
            print(f" ❌ Error saving the configuration: {e}")

    def _load_current_config(self) -> None:
        """Load the current configuration into the UI"""
        if "model" not in st.session_state:
            st.session_state["model"] = os.environ.get("BASE_MODEL_NAME", DEFAULT_CONFIG["model"])
        if "model_url" not in st.session_state:
            st.session_state["model_url"] = os.environ.get("OPENAI_API_BASE", DEFAULT_CONFIG["model_url"])
        if "openai_key" not in st.session_state:
            st.session_state["openai_key"] = os.environ.get("OPENAI_API_KEY", DEFAULT_CONFIG["openai_api_key"])
        if "google_key" not in st.session_state:
            st.session_state["google_key"] = os.environ.get(
                "GOOGLE_SEARCH_API_KEY", DEFAULT_CONFIG["google_search_api_key"]
            )
        if "local" not in st.session_state:
            st.session_state["local"] = os.environ.get("LOCAL", DEFAULT_CONFIG["local"]).lower() == "true"

    def _display_chat_history(self) -> None:
        """Display the chat history in the Streamlit app"""
        for i, message in enumerate(st.session_state.chat_history):
            self._display_message(message)
            st.session_state.chat_history[i] = message

    def _display_message(self, message: dict) -> None:
        """Display a message

        :param dict message: The message to display
        """
        with st.chat_message(message["role"], avatar=message["avatar"]):
            if callable(message["message"]):
                with st.status("Thinking..."):
                    message["message"] = message["message"]()
            st.write(ansi_to_html(message["message"]))

    def _add_to_chat(self, message: Union[str, Callable], is_user: bool = True) -> None:
        """Add a message to the chat history and update the UI

        :param Union[str, Callable] message: The message to add or the method that will create the message
        :param bool is_user: Whether the message is from the user or the bot
        """
        if is_user:
            message = {"role": "You", "message": message, "avatar": "🧑‍💻"}
        else:
            message = {"role": "TechSage", "message": message, "avatar": "🤖"}
        st.session_state.chat_history.append(message)
        self._display_message(message)

    def _send_message(self, message: str) -> None:
        """Send the message that is in the bar

        :param str message: The message to send
        """
        if message.strip() != "":
            self._add_to_chat(message, is_user=True)
            try:
                promise = lambda: self.get_topic_info(message)
                self._add_to_chat(promise, is_user=False)
            except Exception as e:
                error_message = f"❌ An error occurred during the search:\n{e}\n{traceback.format_exc()}"
                self._add_to_chat(error_message, is_user=False)

    def get_topic_info(self, topic: str) -> str:
        """Get the topic info of the current topic using multi agent system

        :param str topic: The topic value
        :return str: The collected info on the topic
        """
        techsage_crew = TechSageCrew(topic)
        result = techsage_crew.run()
        print(result)
        return result


def main() -> None:
    """Main function to run the Streamlit app"""
    TechSageChatApp()


if __name__ == "__main__":
    main()

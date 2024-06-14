import os
import sys
import traceback
from typing import List

import streamlit as st

from techsage.configure import configure
from techsage.crew import TechSageCrew
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

        self.chat_placeholder = st.empty()
        self.chat_history: List[str] = []

        with st.sidebar:
            st.title("Settings")

            st.text_input("Model", key="model")
            st.text_input("Model URL", key="model_url")
            st.text_input("OpenAI API Key", key="openai_key")
            st.text_input("Google Search API Key", key="google_key")
            st.checkbox("Local", key="local")
            col1, col2 = st.columns(2)
            with col1:
                self.setting_button = st.button("Save", on_click=self._save_config)
            with col2:
                self.load_setting_button = st.button("Refresh", on_click=self._load_current_config)

        user_input_col, send_button_col = st.columns([8, 1])
        with user_input_col:
            user_input = st.text_input("Enter a topic:", key="user_input")
        with send_button_col:
            st.button("Send", on_click=self._send_message)

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
            st.session_state["model"] = os.environ.get("BASE_MODEL_NAME", "llama3:8b")
        if "model_url" not in st.session_state:
            st.session_state["model_url"] = os.environ.get("OPENAI_API_BASE", "NA")
        if "openai_key" not in st.session_state:
            st.session_state["openai_key"] = os.environ.get("OPENAI_API_KEY", "NA")
        if "google_key" not in st.session_state:
            st.session_state["google_key"] = os.environ.get("GOOGLE_SEARCH_API_KEY", "NA")
        if "local" not in st.session_state:
            st.session_state["local"] = os.environ.get("LOCAL", "true").lower() == "true"

    def _add_to_chat(self, message: str, is_user: bool = True) -> None:
        """Add a message to the chat history and update the UI

        :param str message: The message to add
        :param bool is_user: Whether the message is from the user or the bot
        """
        if is_user:
            self.chat_history.append(f"**You:** {message}")
        else:
            self.chat_history.append(f"**TechSage:** {ansi_to_html(message)}")
        self._display_chat()

    def _display_chat(self) -> None:
        """Display the chat history in the Streamlit app"""
        with self.chat_placeholder.container():
            for message in self.chat_history:
                st.markdown(message, unsafe_allow_html=True)

    def _send_message(self) -> None:
        """Send the message that is in the bar"""
        if st.session_state.user_input.strip() != "":
            topic = st.session_state.user_input
            self._add_to_chat(topic, is_user=True)
            st.session_state.user_input = ""  # Clear the input field
            try:
                techsage_crew = TechSageCrew(topic)
                result = techsage_crew.run()
                self._add_to_chat(result, is_user=False)
            except Exception as e:
                error_message = f"❌ An error occurred during the search:\n{e}\n{traceback.format_exc()}"
                self._add_to_chat(error_message, is_user=False)


def main() -> None:
    """Main function to run the Streamlit app"""
    TechSageChatApp()


if __name__ == "__main__":
    main()

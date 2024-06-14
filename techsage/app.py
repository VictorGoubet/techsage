import os
import sys
import traceback
from typing import List

import streamlit as st

from techsage.configure import configure
from techsage.crew import TechSageCrew
from techsage.utils.load_config import load_config
from techsage.utils.stream_to_io import _StreamToStringIO


class TechSageChatApp:
    """TechSage Chat Application using Streamlit"""

    def __init__(self) -> None:
        """Initialize the app"""
        self._initialize_streamlit_ui()
        self.original_stdout = sys.stdout

    def _initialize_streamlit_ui(self) -> None:
        """Initialize the Streamlit user interface"""
        st.set_page_config(page_title="TechSage Chat", layout="wide")
        st.title("👋 Welcome to TechSage Information Gatherer")

        self.chat_placeholder = st.empty()
        self.chat_history: List[str] = []

        with st.sidebar:
            st.title("Settings")
            self.model = st.text_input(
                "Model",
                value=self._add_to_state("", "model"),
                key="model",
            )
            self.model_url = st.text_input(
                "Model URL",
                value=self._add_to_state("", "model_url"),
                key="model_url",
            )
            self.openai_key = st.text_input(
                "OpenAI API Key",
                value=self._add_to_state("", "openai_key"),
                key="openai_key",
            )
            self.google_key = st.text_input(
                "Google Search API Key",
                value=self._add_to_state("", "google_key"),
                key="google_key",
            )
            self.local = st.checkbox("Local", value=self._add_to_state(True, "local"), key="local,")
            self.setting_button = st.button("Save", on_click=self._save_config)
            self.load_setting_button = st.button("Load current", on_click=self._load_config)

    def _add_to_state(self, value: str, name: str) -> None:
        """Add a value into the state

        :param str value: The value to add
        :param str name: The name of the value
        """
        if name not in st.session_state:
            st.session_state[name] = value
        return st.session_state[name]

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

    def _load_config(self) -> None:
        """Load the current configuration into the UI"""
        st.session_state["model"] = os.environ.get("OPENAI_MODEL_NAME", "llama3:8b")
        st.session_state["model_url"] = os.environ.get("OPENAI_API_BASE", "NA")
        st.session_state["openai_key"] = os.environ.get("OPENAI_API_KEY", "NA")
        st.session_state["google_key"] = os.environ.get("GOOGLE_SEARCH_API_KEY", "NA")
        st.session_state["local"] = os.environ.get("LOCAL", "true").lower() == "true"

    def _add_to_chat(self, message: str, is_user: bool = True) -> None:
        """Add a message to the chat history and update the UI

        :param str message: The message to add
        :param bool is_user: Whether the message is from the user or the bot
        """
        if is_user:
            self.chat_history.append(f"**You:** {message}")
        else:
            self.chat_history.append(f"**TechSage:** {message}")

        self._display_chat()

    def _display_chat(self) -> None:
        """Display the chat history in the Streamlit app"""
        with self.chat_placeholder.container():
            for message in self.chat_history:
                st.markdown(message)

    def _capture_print_output(self) -> _StreamToStringIO:
        """Capture print output during the execution of a block of code

        :return _StreamToStringIO: The stream to capture print output
        """
        captured_output = _StreamToStringIO()
        sys.stdout = captured_output
        return captured_output

    def _release_print_output(self) -> None:
        """Release the print output capture and restore original stdout"""
        sys.stdout = self.original_stdout

    def run(self) -> None:
        """Run the chat application"""
        user_input = st.text_input("Your message:", key="user_input")
        if user_input:
            self._add_to_chat(user_input, is_user=True)
            try:
                topic = user_input
                techsage_crew = TechSageCrew(topic)
                captured_output = self._capture_print_output()
                result = techsage_crew.run()
                self._release_print_output()
                print_output = captured_output.getvalue()
                self._add_to_chat(print_output, is_user=False)
                self._add_to_chat(result, is_user=False)
            except Exception as e:
                error_message = f"❌ An error occurred during the search:\n{e}\n{traceback.format_exc()}"
                self._add_to_chat(error_message, is_user=False)


def main() -> None:
    """Main function to run the Streamlit app"""
    app = TechSageChatApp()
    app.run()


if __name__ == "__main__":
    main()

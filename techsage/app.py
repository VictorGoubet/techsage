import sys
import traceback
from typing import List

import streamlit as st

from techsage.crew import TechSageCrew
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
        self.chat_placeholder = st.empty()
        self.chat_history: List[str] = []

        with st.sidebar:
            st.title("Settings")
            self.api_key = st.text_input("OpenAI API Key", type="password")

        st.title("👋 Welcome to TechSage Information Gatherer")
        st.write("Enter a topic below to get started:")

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

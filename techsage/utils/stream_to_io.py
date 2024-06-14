import io


class _StreamToStringIO:
    """Redirect print statements to StringIO for capturing output"""

    def __init__(self):
        self.output = io.StringIO()

    def write(self, message: str) -> None:
        """Write message to StringIO

        :param str message: The message to write
        """
        self.output.write(message)

    def flush(self) -> None:
        """Flush the StringIO buffer"""
        self.output.flush()

    def getvalue(self) -> str:
        """Get the current value of the StringIO buffer

        :return str: The captured output
        """
        return self.output.getvalue()

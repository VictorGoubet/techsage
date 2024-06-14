import re


def ansi_to_html(text: str) -> str:
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    text = ansi_escape.sub("", text)  # Remove all ANSI escape codes
    # Replace specific ANSI codes with HTML tags (you can expand this as needed)
    text = text.replace("[1m", "<b>").replace("[0m", "</b>")  # Bold
    text = text.replace("[95m", '<span style="color: magenta;">').replace("[00m", "</span>")  # Magenta
    return text

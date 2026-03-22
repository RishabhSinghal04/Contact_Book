from typing import TypeVar

from core.interfaces import IOutputHandler

T = TypeVar("T")


def options_display(
    options: dict[T, str],
    output_handler: IOutputHandler,
    separator: str = "\n",
    border_char: str = "-",
) -> None:
    """
    Display menu options with border.

    Args:
        :
        options (dict[T, str]): Mapping of option keys to their display labels.
        output_handler (IOutputHandler): Handler responsible for displaying the output.
        separator (str, optional): String used to separate menu items. Defaults to newline.
        border_char (str, optional): Character used to draw the border line. Defaults to "-".
    """
    message = separator.join(
        f"{index}. {format_label(option)}" for index, option in options.items()
    )

    border = border_line(message, separator, border_char)
    text = f"{border}\n{message}\n{border}"

    output_handler.display(text)


def format_label(text: str) -> str:
    """Convert underscore-separated text into capitalized words with spaces."""
    return " ".join(word.capitalize() for word in text.split("_"))


def border_line(text: str, separator: str, border_char: str) -> str:
    if separator == "\n":
        lines: list[str] = [line.strip() for line in text.split("\n") if line.strip()]
        return border_char * (len(max(lines, key=len)) + 1)

    return border_char * (len(text) + 1)

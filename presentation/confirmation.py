from core.interfaces import IOutputHandler
from presentation.input_handler import UserInputHandler
from presentation.key_map import CONFIRMATION_KEY_MAP, confirmation_key_map
from presentation.cli.options_display import options_display


def confirm_action(
    input_handler: UserInputHandler,
    output_handler: IOutputHandler,
    message: str = "Select an option: ",
)  -> bool:
    """
    Prompt user for Yes/No confirmation.

    Args:
        input_handler: For user input.
        message: Optional custom prompt message.

    Returns:
        bool: True if user selected Yes, False if No.
    """
    options_display(
        confirmation_key_map, output_handler, " " * len(confirmation_key_map)
    )
    choice: str = input_handler.get_action(message, confirmation_key_map)
    return choice == CONFIRMATION_KEY_MAP.YES.value

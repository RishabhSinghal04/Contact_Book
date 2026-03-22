import sys
import re
from typing import Callable, Optional, TypeVar
from functools import lru_cache

from core.interfaces import IOutputHandler
from presentation.output_handler import ConsoleOutputHandler

try:
    import winsound
except ImportError:
    winsound = None

T = TypeVar("T")
K = TypeVar("K")


class UserInputHandler:

    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output_handler: Optional[IOutputHandler] = None,
    ) -> None:
        self.input_func: Callable[[str], str] = input_func
        self.output_handler: IOutputHandler = output_handler or ConsoleOutputHandler()

    def get_action(self, prompt: str, key_map: dict[K, str]) -> K:
        """
        Prompt the user until they enter a valid key from the given key_map.

        Args:
            prompt (str): Message shown to the user.
            key_map (dict[K, str]): Mapping of valid keys to actions.

        Returns:
            K: The valid key chosen by the user (normalized to lowercase).
        """
        valid_keys = list(key_map.keys())
        return self._get_validated_input(
            prompt,
            lambda v: (
                next((k for k in valid_keys if str(k).lower() == v.lower()), None)
                if v
                else None
            ),
            "Invalid Input! Valid Key(s): " + ", ".join(map(str, valid_keys)),
        )

    def get_string(self, prompt: str, num_of_chars: int = 12) -> str:
        """
        Prompt the user until they enter a non-empty string.

        Args:
            prompt (str): Message shown to the user.
            num_of_chars (int): Maximum allowed length for the input string (default: 12).

        Returns:
            str: A valid non-empty string entered by the user.
        """
        pattern = UserInputHandler._default_string_pattern()
        return self._get_validated_input(
            prompt,
            lambda v: v if v and len(v) <= num_of_chars and pattern.match(v) else None,
            f"Invalid Input! Please use only letters, numbers, spaces, and . , ! ? - (max {num_of_chars} characters).",
            use_strip=True,
        )

    # ___internal helpers___
    @staticmethod
    @lru_cache(maxsize=1)
    def _default_string_pattern() -> re.Pattern[str]:
        return re.compile(r"^[a-zA-Z0-9\s.,!?+@()\-]+$", re.UNICODE)

    def _get_validated_input(
        self,
        prompt: str,
        validator: Callable[[str], Optional[T]],
        error_message: str,
        use_strip: bool = False,
    ) -> T:
        """
        Internal helper: repeatedly prompt until validator returns a non-None value.
        If use_strip=True, input is trimmed before validation.
        Displays error_message once if input is invalid.
        """
        show_invalid = False
        while True:
            raw_value = self.input_func(prompt)
            if use_strip:
                raw_value: str = raw_value.strip()
            result: Optional[T] = validator(raw_value)
            if result is not None:
                return result
            self._beep()
            if not show_invalid:
                self.output_handler.display(error_message)
                show_invalid = True

    def _beep(self) -> None:
        # winsound.Beep(1000, 300)
        if winsound:
            winsound.MessageBeep()
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()

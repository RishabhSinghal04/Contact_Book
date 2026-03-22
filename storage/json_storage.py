import json
from pathlib import Path

from core.interfaces import IStorageBackend

from utils.exceptions import StorageError
from utils.logger import get_logger


logger = get_logger(__name__)


class JsonStorage(IStorageBackend):
    def __init__(self, filepath: str = "data/contacts.json") -> None:
        """
        Initialize the storage backend with a given file path.

        Args:
            filepath (str): Path to the JSON file. Defaults to "data/contacts.json".

        Raises:
            StorageError: If the storage file or directory cannot be created.
        """
        self.filepath = Path(filepath)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Ensure that the storage file and its parent directory exist.

        - Creates the parent directory if missing.
        - Creates an empty JSON file if missing.
        - Logs creation events.

        Raises:
            StorageError: If the directory or file cannot be created.
        """
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            if not self.filepath.exists():
                self.write([])
                logger.info(f"Created new storage file: {self.filepath}")
        except OSError as e:
            message = f"Failed to create storage: {e}"
            logger.error(message)
            raise StorageError(message)

    def read(self):
        """
        Read raw data from the JSON file.

        Returns:
            list: A list of contact records. Returns an empty list if the file is empty or not found.

        Raises:
            StorageError: If the JSON file is corrupted.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            logger.warning(f"File not found: {self.filepath}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON file: {e}")
            raise StorageError(f"Corrupted data in {self.filepath}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading file: {e}")
            raise StorageError(f"Failed to read {self.filepath}: {e}")

    def write(self, data: list[dict]) -> None:
        """
        Write raw data to the JSON file.

        Args:
            data (list[dict]): A list of contact records to persist.

        Raises:
            StorageError: If writing to the file fails.
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to write data: {e}")
            raise StorageError(f"Failed to write: {e}")

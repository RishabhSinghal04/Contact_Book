from kivy.uix.label import Label
from kivy.uix.popup import Popup

from presentation.gui.app import ContactBookApp
from repositories.contact_repository import ContactRepository
from storage.json_storage import JsonStorage
from utils.logger import get_logger

logger = get_logger(__name__)


def show_error_dialog(message: str) -> None:
    """Show error in Kivy popup (if Kivy is initialized)"""
    try:
        popup = Popup(
            title="Fatal Error", content=Label(text=message), size_hint=(0.8, 0.4)
        )
        popup.open()
    except Exception:
        print(f"ERROR: {message}")


def main() -> int:
    try:
        storage = JsonStorage("data/contacts.json")
        repository = ContactRepository(storage)

    except Exception as e:
        print(f"FATAL: Cannot initialize backend - {e}")
        logger.exception("Backend initialization failed")
        return 1

    try:
        app = ContactBookApp(repository)
        app.run()

    except Exception as e:
        error_msg = f"Application crashed: {e}"
        print(f"FATAL: {error_msg}")
        logger.exception("Application crashed")

        try:
            show_error_dialog(error_msg)
        except:
            pass

        return 1

    return 0


if __name__ == "__main__":
    exit(main())

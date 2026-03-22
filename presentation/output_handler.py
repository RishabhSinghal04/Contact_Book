from core.interfaces import IOutputHandler


class ConsoleOutputHandler(IOutputHandler):
    def display(self, message: str, separator: str = "\n") -> None:
        print(message, end=separator)

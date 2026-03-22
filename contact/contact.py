from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Contact:
    name: str
    phone_num: str
    email: Optional[str] = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Contact):
            return NotImplemented
        return self.phone_num == other.phone_num

    def __hash__(self) -> int:
        return hash(self.phone_num)

    def __str__(self) -> str:
        email_str = f" | {self.email}" if self.email else ""
        return f"{self.name}: {self.phone_num}{email_str}"

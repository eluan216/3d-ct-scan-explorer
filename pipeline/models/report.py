"""
Structured pipeline messages with severity levels.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Message:
    severity: Severity
    code: str
    text: str

    def __str__(self) -> str:
        return f"{self.severity.value}: [{self.code}] {self.text}"


@dataclass
class Report:
    messages: List[Message] = field(default_factory=list)

    def add(self, severity: Severity, code: str, text: str) -> None:
        self.messages.append(Message(severity, code, text))

    def error(self, code: str, text: str) -> None:
        self.add(Severity.ERROR, code, text)

    def warning(self, code: str, text: str) -> None:
        self.add(Severity.WARNING, code, text)

    def info(self, code: str, text: str) -> None:
        self.add(Severity.INFO, code, text)

    @property
    def has_errors(self) -> bool:
        return any(m.severity == Severity.ERROR for m in self.messages)

    @property
    def errors(self) -> List[Message]:
        return [m for m in self.messages if m.severity == Severity.ERROR]

    @property
    def warnings(self) -> List[Message]:
        return [m for m in self.messages if m.severity == Severity.WARNING]

    def summary(self) -> str:
        lines = [str(m) for m in self.messages]
        return "\n".join(lines) if lines else "No messages."

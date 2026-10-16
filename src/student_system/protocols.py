"""Structural interfaces (Protocols)."""

from collections.abc import Iterable
from typing import Protocol

from student_system.models import Student
from student_system.value_objects import Grade


class Notifier(Protocol):
    """Notification interface."""

    def send(self, recipient: str, message: str) -> None: ...


class Exporter(Protocol):
    """Export interface."""

    def export(self, students: Iterable[Student]) -> str: ...


class GradePolicy(Protocol):
    """Grade adjustment policy."""

    def apply(self, grade: Grade) -> Grade: ...
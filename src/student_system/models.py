"""Domain entities."""

from dataclasses import dataclass

from student_system.exceptions import ValidationError
from student_system.value_objects import Grade


@dataclass(slots=True)
class Student:
    """Domain entity for a student."""

    student_id: int
    first_name: str
    last_name: str
    group: str
    grade: Grade

    def __post_init__(self) -> None:
        if self.student_id <= 0:
            raise ValidationError("student_id must be positive")
        if not self.first_name.strip():
            raise ValidationError("first_name must not be empty")
        if not self.last_name.strip():
            raise ValidationError("last_name must not be empty")
        if not self.group.strip():
            raise ValidationError("group must not be empty")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return (
            f"Student(id={self.student_id}, "
            f"name={self.full_name!r}, "
            f"group={self.group!r}, "
            f"grade={self.grade})"
        )

    def __str__(self) -> str:
        return (
            f"{self.student_id:>4}  "
            f"{self.full_name:<25}"
            f"{self.group:<8}"
            f"{self.grade.value:>7.2f}"
                            )
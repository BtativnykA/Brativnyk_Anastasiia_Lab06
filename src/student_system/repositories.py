"""Repository abstraction and in-memory implementation."""

from abc import ABC, abstractmethod

from student_system.exceptions import DuplicateError, NotFoundError
from student_system.models import Student


class StudentRepository(ABC):
    """Abstract repository."""

    @abstractmethod
    def add(self, student: Student) -> None: ...

    @abstractmethod
    def get(self, student_id: int) -> Student | None: ...

    @abstractmethod
    def all(self) -> list[Student]: ...

    @abstractmethod
    def remove(self, student_id: int) -> bool: ...


class InMemoryStudentRepository(StudentRepository):
    """In-memory repository keyed by student_id."""

    def __init__(self) -> None:
        self._items: dict[int, Student] = {}

    def add(self, student: Student) -> None:
        if student.student_id in self._items:
            raise DuplicateError(
                f"Student {student.student_id} already exists"
            )
        self._items[student.student_id] = student

    def get(self, student_id: int) -> Student | None:
        return self._items.get(student_id)

    def require(self, student_id: int) -> Student:
        student = self._items.get(student_id)
        if student is None:
            raise NotFoundError(f"Student {student_id} not found")
        return student

    def all(self) -> list[Student]:
        return list(self._items.values())

    def remove(self, student_id: int) -> bool:
        return self._items.pop(student_id, None) is not None

    def __len__(self) -> int:
        return len(self._items)
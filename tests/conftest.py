"""Shared pytest fixtures."""

from collections.abc import Iterator

import pytest

from student_system.models import Student
from student_system.repositories import InMemoryStudentRepository
from student_system.value_objects import Grade


@pytest.fixture
def student() -> Student:
    """A single demo student."""
    return Student(
        student_id=1,
        first_name="Anna",
        last_name="Koval",
        group="PI-21",
        grade=Grade(91.5),
    )


@pytest.fixture
def students() -> list[Student]:
    """Three demo students in different groups."""
    return [
        Student(1, "Anna", "Koval", "PI-21", Grade(91.5)),
        Student(2, "Oleh", "Melnyk", "PI-21", Grade(84.0)),
        Student(3, "Iryna", "Bondar", "PI-22", Grade(95.2)),
    ]


@pytest.fixture
def repository(students: list[Student]) -> Iterator[InMemoryStudentRepository]:
    """Pre-populated repository (fixture with yield for cleanup)."""
    repo = InMemoryStudentRepository()
    for s in students:
        repo.add(s)
    yield repo
    # teardown: nothing to clean since it's in-memory
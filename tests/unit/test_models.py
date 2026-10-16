"""Unit tests for Student entity."""

import pytest

from student_system.exceptions import ValidationError
from student_system.models import Student
from student_system.value_objects import Grade


def test_student_creation(student: Student) -> None:
    assert student.student_id == 1
    assert student.full_name == "Anna Koval"
    assert student.group == "PI-21"
    assert student.grade.value == pytest.approx(91.5)


def test_student_str_format(student: Student) -> None:
    text = str(student)
    assert "Anna Koval" in text
    assert "PI-21" in text
    assert "91.50" in text


def test_student_repr(student: Student) -> None:
    text = repr(student)
    assert "Student(" in text
    assert "id=1" in text


def test_student_invalid_id() -> None:
    with pytest.raises(ValidationError, match="student_id"):
        Student(0, "A", "B", "PI-21", Grade(80.0))


def test_student_empty_first_name() -> None:
    with pytest.raises(ValidationError, match="first_name"):
        Student(1, "  ", "B", "PI-21", Grade(80.0))


def test_student_empty_last_name() -> None:
    with pytest.raises(ValidationError, match="last_name"):
        Student(1, "A", "", "PI-21", Grade(80.0))


def test_student_empty_group() -> None:
    with pytest.raises(ValidationError, match="group"):
        Student(1, "A", "B", "   ", Grade(80.0))
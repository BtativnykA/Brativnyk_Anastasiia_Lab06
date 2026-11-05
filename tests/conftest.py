import pytest
from unittest.mock import Mock
from reliable_importer.models import Student

@pytest.fixture
def sample_student() -> Student:
    return Student(
        student_id=1, name="Anna Koval", group="PI-21", grade=91.5, email="anna@test.com"
    )

@pytest.fixture
def sample_students() -> list[Student]:
    return [
        Student(1, "Anna Koval", "PI-21", 91.5, "anna@test.com"),
        Student(2, "Oleh Melnyk", "PI-21", 84.0, "oleh@test.com"),
        Student(3, "Iryna Bondar", "PI-22", 95.2, "iryna@test.com"),
    ]

@pytest.fixture
def mock_notifier():
    return Mock()
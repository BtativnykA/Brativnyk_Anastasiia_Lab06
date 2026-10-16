"""Unit tests for StudentService using Mock."""

from unittest.mock import Mock

import pytest

from student_system.exceptions import (
    DuplicateError,
    ExternalServiceError,
    NotFoundError,
)
from student_system.models import Student
from student_system.protocols import Exporter, GradePolicy, Notifier
from student_system.repositories import InMemoryStudentRepository
from student_system.services import StudentService
from student_system.value_objects import Grade


@pytest.fixture
def service(repository: InMemoryStudentRepository) -> StudentService:
    """Service with mocked dependencies."""
    notifier = Mock(spec=Notifier)
    exporter = Mock(spec=Exporter)
    exporter.export.return_value = "[]"
    policy = Mock(spec=GradePolicy)
    policy.apply.side_effect = lambda g: g  # identity
    return StudentService(repository, notifier, exporter, policy)


def test_register_adds_student(service: StudentService) -> None:
    new_student = Student(10, "Petro", "Novak", "PI-23", Grade(88.0))
    result = service.register(new_student)
    assert result.student_id == 10
    assert service._repo.get(10) is not None  # type: ignore[attr-defined]


def test_register_sends_notification(service: StudentService) -> None:
    new_student = Student(10, "Petro", "Novak", "PI-23", Grade(88.0))
    service.register(new_student)
    notifier = service._notifier  # type: ignore[attr-defined]
    notifier.send.assert_called_once_with(
        "registry@university",
        "Registered: Petro Novak",
    )


def test_register_duplicate_raises(service: StudentService) -> None:
    duplicate = Student(1, "Anna", "Koval", "PI-21", Grade(91.5))
    with pytest.raises(DuplicateError):
        service.register(duplicate)


def test_register_notifier_failure_wraps_error(
    repository: InMemoryStudentRepository,
) -> None:
    notifier = Mock(spec=Notifier)
    notifier.send.side_effect = RuntimeError("network down")
    exporter = Mock(spec=Exporter)
    policy = Mock(spec=GradePolicy)
    policy.apply.side_effect = lambda g: g

    service = StudentService(repository, notifier, exporter, policy)
    new_student = Student(20, "Taras", "Shevchenko", "PI-23", Grade(90.0))
    with pytest.raises(ExternalServiceError, match="Notifier failed"):
        service.register(new_student)


def test_find_by_last_name(service: StudentService) -> None:
    result = service.find_by_last_name("koval")
    assert len(result) == 1
    assert result[0].first_name == "Anna"


def test_find_by_last_name_not_found(service: StudentService) -> None:
    assert service.find_by_last_name("Nonexistent") == []


def test_filter_by_group(service: StudentService) -> None:
    result = service.filter_by_group("PI-21")
    assert len(result) == 2


def test_filter_by_group_empty(service: StudentService) -> None:
    assert service.filter_by_group("PI-99") == []


def test_best_student(service: StudentService) -> None:
    best = service.best_student()
    assert best is not None
    assert best.first_name == "Iryna"


def test_best_student_empty_repository() -> None:
    from unittest.mock import Mock as M

    from student_system.protocols import Exporter, GradePolicy, Notifier

    repo = InMemoryStudentRepository()
    service = StudentService(
        repo,
        M(spec=Notifier),
        M(spec=Exporter),
        M(spec=GradePolicy),
    )
    assert service.best_student() is None


def test_average_of_group(service: StudentService) -> None:
    avg = service.average_of_group("PI-21")
    assert avg == pytest.approx((91.5 + 84.0) / 2)


def test_average_of_empty_group(service: StudentService) -> None:
    assert service.average_of_group("PI-99") == 0.0


def test_update_grade(service: StudentService) -> None:
    updated = service.update_grade(1, Grade(95.0))
    assert updated.grade.value == pytest.approx(95.0)
    assert service._repo.get(1).grade.value == pytest.approx(95.0)  # type: ignore[union-attr,attr-defined]


def test_update_grade_not_found(service: StudentService) -> None:
    with pytest.raises(NotFoundError):
        service.update_grade(999, Grade(90.0))


def test_export_all_uses_exporter(service: StudentService) -> None:
    service.export_all()
    exporter = service._exporter  # type: ignore[attr-defined]
    exporter.export.assert_called_once()


@pytest.mark.parametrize(
    ("group", "expected"),
    [
        ("PI-21", 2),
        ("PI-22", 1),
        ("PI-99", 0),
    ],
)
def test_group_counts(service: StudentService, group: str, expected: int) -> None:
    assert len(service.filter_by_group(group)) == expected
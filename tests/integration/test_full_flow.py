"""Integration test: service + repository + exporter + notifier."""

from unittest.mock import Mock

import pytest

from student_system.models import Student
from student_system.protocols import Exporter, GradePolicy, Notifier
from student_system.repositories import InMemoryStudentRepository
from student_system.services import StudentService
from student_system.value_objects import Grade


@pytest.mark.integration
def test_full_student_lifecycle() -> None:
    repo = InMemoryStudentRepository()
    notifier = Mock(spec=Notifier)
    exporter = Mock(spec=Exporter)
    exporter.export.return_value = "EXPORTED"
    policy = Mock(spec=GradePolicy)
    policy.apply.side_effect = lambda g: g

    service = StudentService(repo, notifier, exporter, policy)

    # register
    s = Student(1, "Anna", "Koval", "PI-21", Grade(91.5))
    service.register(s)
    assert len(repo) == 1
    notifier.send.assert_called_once()

    # update
    updated = service.update_grade(1, Grade(95.0))
    assert updated.grade.value == pytest.approx(95.0)

    # queries
    assert service.best_student() is updated
    assert service.average_of_group("PI-21") == pytest.approx(95.0)

    # export
    service.export_all()
    exporter.export.assert_called_once()


@pytest.mark.integration
def test_register_duplicate_through_service() -> None:
    from student_system.exceptions import DuplicateError

    repo = InMemoryStudentRepository()
    service = StudentService(
        repo,
        Mock(spec=Notifier),
        Mock(spec=Exporter),
        Mock(spec=GradePolicy),
    )
    service._policy.apply.side_effect = lambda g: g  # type: ignore[attr-defined]

    s = Student(1, "Anna", "Koval", "PI-21", Grade(90.0))
    service.register(s)
    with pytest.raises(DuplicateError):
        service.register(s)
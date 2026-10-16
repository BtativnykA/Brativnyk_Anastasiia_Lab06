"""Application service layer."""

import logging

from student_system.exceptions import ExternalServiceError
from student_system.models import Student
from student_system.protocols import Exporter, GradePolicy, Notifier
from student_system.repositories import StudentRepository
from student_system.value_objects import Grade

logger = logging.getLogger(__name__)


class StudentService:
    """Orchestrates student use cases."""

    def __init__(
        self,
        repository: StudentRepository,
        notifier: Notifier,
        exporter: Exporter,
        policy: GradePolicy,
    ) -> None:
        self._repo = repository
        self._notifier = notifier
        self._exporter = exporter
        self._policy = policy

    def register(self, student: Student) -> Student:
        adjusted = Student(
            student_id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            group=student.group,
            grade=self._policy.apply(student.grade),
        )
        self._repo.add(adjusted)
        try:
            self._notifier.send(
                "registry@university",
                f"Registered: {adjusted.full_name}",
            )
        except Exception as error:
            raise ExternalServiceError(
                "Notifier failed"
            ) from error
        return adjusted

    def find_by_last_name(self, last_name: str) -> list[Student]:
        needle = last_name.strip().lower()
        return [
            s for s in self._repo.all()
            if s.last_name.lower() == needle
        ]

    def filter_by_group(self, group: str) -> list[Student]:
        return [s for s in self._repo.all() if s.group == group]

    def best_student(self) -> Student | None:
        students = self._repo.all()
        if not students:
            return None
        return max(students, key=lambda s: s.grade.value)

    def average_of_group(self, group: str) -> float:
        students = self.filter_by_group(group)
        if not students:
            return 0.0
        total = sum(s.grade.value for s in students)
        return total / len(students)

    def update_grade(
        self, student_id: int, new_grade: Grade
    ) -> Student:
        student = self._repo.require(student_id)
        adjusted = self._policy.apply(new_grade)
        updated = Student(
            student_id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            group=student.group,
            grade=adjusted,
        )
        self._repo.remove(student_id)
        self._repo.add(updated)
        return updated

    def export_all(self) -> str:
        return self._exporter.export(self._repo.all())


def main() -> None:
    """Entry point — only used for manual demo."""
    from student_system.repositories import InMemoryStudentRepository

    class _Noop:
        def send(self, recipient: str, message: str) -> None:
            print(f"[notify] {recipient}: {message}")

        def export(self, students) -> str:
            return "\n".join(str(s) for s in students)

        def apply(self, grade: Grade) -> Grade:
            return grade

    repo = InMemoryStudentRepository()
    service = StudentService(repo, _Noop(), _Noop(), _Noop())
    service.register(Student(1, "Anna", "Koval", "PI-21", Grade(91.5)))
    print(service.export_all())
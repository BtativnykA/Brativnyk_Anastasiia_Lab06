"""Async service that depends on an external client."""

from student_system.exceptions import ExternalServiceError
from student_system.models import Student


class AsyncStudentClient:
    """Wraps an async external client."""

    def __init__(self, client: object) -> None:
        self._client = client

    async def fetch_student(self, student_id: int) -> Student:
        try:
            data = await self._client.fetch(student_id)
        except Exception as error:
            raise ExternalServiceError(
                f"Cannot fetch student {student_id}"
            ) from error

        from student_system.value_objects import Grade

        return Student(
            student_id=data["student_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            group=data["group"],
            grade=Grade(data["grade"]),
        )
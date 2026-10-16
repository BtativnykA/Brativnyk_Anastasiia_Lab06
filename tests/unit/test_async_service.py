"""Unit tests for AsyncStudentClient using AsyncMock."""

from unittest.mock import AsyncMock

import pytest

from student_system.async_service import AsyncStudentClient
from student_system.exceptions import ExternalServiceError


@pytest.fixture
def fake_data() -> dict:
    return {
        "student_id": 1,
        "first_name": "Anna",
        "last_name": "Koval",
        "group": "PI-21",
        "grade": 91.5,
    }


async def test_fetch_student_success(fake_data: dict) -> None:
    client = AsyncMock()
    client.fetch.return_value = fake_data

    service = AsyncStudentClient(client)
    student = await service.fetch_student(1)

    assert student.student_id == 1
    assert student.first_name == "Anna"
    client.fetch.assert_awaited_once_with(1)


async def test_fetch_student_failure_wraps_error() -> None:
    client = AsyncMock()
    client.fetch.side_effect = ConnectionError("network down")

    service = AsyncStudentClient(client)

    with pytest.raises(ExternalServiceError, match="Cannot fetch"):
        await service.fetch_student(1)

    client.fetch.assert_awaited_once_with(1)
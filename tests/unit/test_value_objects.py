"""Unit tests for Grade value object."""

import pytest

from student_system.value_objects import Grade


def test_grade_creation() -> None:
    g = Grade(90.0)
    assert g.value == 90.0


def test_negative_grade_rejected() -> None:
    with pytest.raises(ValueError, match="Grade must be in"):
        Grade(-1.0)


def test_grade_above_100_rejected() -> None:
    with pytest.raises(ValueError, match="Grade must be in"):
        Grade(100.1)


def test_grade_average_with_add() -> None:
    result = Grade(80.0) + Grade(90.0)
    assert result.value == pytest.approx(85.0)


def test_grade_ordering() -> None:
    assert Grade(80.0) < Grade(90.0)
    assert not (Grade(90.0) < Grade(80.0))


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        pytest.param(0.0, 0.0, id="minimum"),
        pytest.param(50.0, 50.0, id="middle"),
        pytest.param(99.99, 99.99, id="near-max"),
        pytest.param(100.0, 100.0, id="maximum"),
    ],
)
def test_valid_grade_boundaries(raw: float, expected: float) -> None:
    assert Grade(raw).value == pytest.approx(expected)


@pytest.mark.parametrize(
    "raw",
    [-0.01, 100.01, -100.0, 1000.0],
)
def test_invalid_grade_boundaries(raw: float) -> None:
    with pytest.raises(ValueError):
        Grade(raw)
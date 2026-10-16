"""Unit tests for JsonExporter."""

import json

import pytest

from student_system.exporters import JsonExporter, export_students_to_file
from student_system.models import Student


def test_export_single_student(student: Student) -> None:
    text = JsonExporter().export([student])
    data = json.loads(text)
    assert len(data) == 1
    assert data[0]["student_id"] == 1
    assert data[0]["name"] == "Anna Koval"
    assert data[0]["grade"] == pytest.approx(91.5)


def test_export_empty_list() -> None:
    text = JsonExporter().export([])
    assert json.loads(text) == []


def test_export_multiple_students(students: list[Student]) -> None:
    text = JsonExporter().export(students)
    data = json.loads(text)
    assert len(data) == 3


def test_export_to_file(tmp_path, students: list[Student]) -> None:
    output = tmp_path / "students.json"
    count = export_students_to_file(students, output)
    assert count == 3
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 3


def test_export_to_file_creates_valid_json(tmp_path, student: Student) -> None:
    output = tmp_path / "single.json"
    export_students_to_file([student], output)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data[0]["group"] == "PI-21"
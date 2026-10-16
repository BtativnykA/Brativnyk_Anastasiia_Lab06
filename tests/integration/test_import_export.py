"""Integration test: end-to-end import → export."""

import json

import pytest

from student_system.exporters import export_students_to_file
from student_system.models import Student
from student_system.value_objects import Grade


@pytest.mark.integration
def test_full_import_export_flow(tmp_path) -> None:
    students = [
        Student(1, "Anna", "Koval", "PI-21", Grade(91.5)),
        Student(2, "Oleh", "Melnyk", "PI-21", Grade(84.0)),
        Student(3, "Iryna", "Bondar", "PI-22", Grade(95.2)),
    ]

    output = tmp_path / "export.json"
    count = export_students_to_file(students, output)

    assert count == 3
    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 3
    assert data[0]["name"] == "Anna Koval"
    assert data[2]["grade"] == pytest.approx(95.2)


@pytest.mark.integration
def test_export_preserves_order(tmp_path, students) -> None:
    output = tmp_path / "ordered.json"
    export_students_to_file(students, output)
    data = json.loads(output.read_text(encoding="utf-8"))
    ids = [row["student_id"] for row in data]
    assert ids == [1, 2, 3]
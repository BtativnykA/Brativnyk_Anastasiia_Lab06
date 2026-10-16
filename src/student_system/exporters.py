"""JSON exporters."""

import json
from collections.abc import Iterable
from pathlib import Path

from student_system.models import Student


class JsonExporter:
    """Exports students to JSON format."""

    def export(self, students: Iterable[Student]) -> str:
        return json.dumps(
            [self._to_dict(s) for s in students],
            ensure_ascii=False,
            indent=2,
        )

    @staticmethod
    def _to_dict(student: Student) -> dict[str, object]:
        return {
            "student_id": student.student_id,
            "name": student.full_name,
            "group": student.group,
            "grade": student.grade.value,
        }


def export_students_to_file(
    students: Iterable[Student],
    path: Path,
) -> int:
    """Write students to a JSON file, return count."""
    items = list(students)
    exporter = JsonExporter()
    text = exporter.export(items)
    path.write_text(text, encoding="utf-8")
    return len(items)
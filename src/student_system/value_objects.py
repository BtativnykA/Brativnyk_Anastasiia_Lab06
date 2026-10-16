"""Immutable value objects."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grade:
    """A validated immutable grade in [0, 100]."""

    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 100.0:
           raise ValueError(
                f"Grade must be in [0, 100], got {self.value}"
            )

    def __add__(self, other: "Grade") -> "Grade":
        return Grade((self.value + other.value) / 2)

    def __lt__(self, other: "Grade") -> bool:
        return self.value < other.value

    def __str__(self) -> str:
        return f"{self.value:.2f}"
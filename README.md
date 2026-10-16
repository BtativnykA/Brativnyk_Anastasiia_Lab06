# Student System (Lab06)

Лабораторна робота №6 з курсу «Професійний Python».
Варіант №1 — «Система обліку студентів».

## Description

Production-код + pytest test suite: unit + integration tests,
fixtures, parametrization, Mock, AsyncMock, tmp_path, monkeypatch,
coverage + branch coverage.

## Run tests

```bash
python -m pytest -v
Run with coverage
bash
python -m pytest \
    --cov=student_system \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html
Project structure
text
src/student_system/   — production code
tests/unit/           — unit tests (fast, isolated)
tests/integration/    — integration tests (real filesystem)
tests/conftest.py     — shared fixtures
Author
Student: Anastasiia Brativnyk
Group: ФеП-32
Lab: №6, Variant 1

text

---

```bash
cd ~/Desktop/Brativnyk_Anastasiia_Lab06
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

# запустити всі тести
python -m pytest -v
Очікуваний результат: усі тести passed (приблизно 40+ тестів).

Потім з coverage:

bash
python -m pytest \
    --cov=student_system \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html
Маєш побачити таблицю coverage + папку htmlcov/.
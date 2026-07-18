vendingMachine

Small Python OOP example project: a minimal `VendingMachine` package with tests.

Setup
-----

1. Create a virtual environment and activate it

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dev/test requirements

```powershell
pip install -r requirements.txt
```

Run tests
---------

```powershell
pytest -q
```

Quick usage
-----------
Make terminal location .example_runs

At terminal type:
>> python <filename>

Project layout
--------------

Root files:

- `requirements.txt` — test requirements
- `.gitignore` — common Python ignores

Code and tests:

- `src/vending_machine/` — package code
- `tests/` — pytest tests

Notes
-----

This repository is intentionally small and focused on a clean, testable OOP layout. Add more modules under `src/vending_machine` and corresponding tests under `tests/` as the project grows.

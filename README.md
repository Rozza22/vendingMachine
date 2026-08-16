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

CLI Menu
--------------
Run the following:
>> python -m vending_machine.cli

You will need to enter Admin menu first to stock some products before being able to simulate customer purchases using the Customer menu

Project layout
--------------

Root files:

- `requirements.txt` — test requirements
- `.gitignore` — common Python ignores

Code and tests:

- `src/vending_machine/` — package code
- `tests/` — pytest tests

Metrics:
- Gross Profit is the amount of money incoming to the vending machine through sales
- Stock Investment is the amount of money spent on stock
- Transaction history contains all customer purchases and the details on these

Notes
-----

This repository is intentionally small and focused on a clean, testable OOP layout. Add more modules under `src/vending_machine` and corresponding tests under `tests/` as the project grows.

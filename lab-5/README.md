# Lab 5 - Bank Account System

This folder contains a revised version of the assigned bank account script and a record of the issues addressed.

## Run

```bash
python bank_account_system.py
```

## Install and run the lab tools

```bash
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8

# Baseline reports should be generated from the original source before fixes.
# Run the tools on this revised source for the after reports:
pylint bank_account_system.py > pylint_report_after.txt
bandit -r bank_account_system.py > bandit_report_after.txt
flake8 bank_account_system.py > flake8_report_after.txt
```

See `ISSUE_TABLE.md` for the issue/fix record and reflection. The source handout asks for three separate commits, one corresponding to fixes from each tool, and before/after reports. Those repository commits have not been made from this workspace.

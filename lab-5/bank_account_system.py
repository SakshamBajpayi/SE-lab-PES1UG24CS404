"""Bank account management module."""

import ast
import hashlib
import hmac
import os
import secrets

account_data = {}


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create an account and optionally record its creation."""
    if acc_id in account_data or initial_deposit < 0:
        return False

    if transactions is None:
        transactions = []

    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id, amount):
    """Deposit a positive amount into an existing account."""
    if acc_id not in account_data or amount <= 0:
        return False

    account_data[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw a positive amount when sufficient funds are available."""
    if acc_id not in account_data or amount <= 0:
        return False

    if account_data[acc_id]["balance"] < amount:
        return False

    account_data[acc_id]["balance"] -= amount
    return True


def _evaluate_bonus_expression(expression, balance):
    """Evaluate a limited arithmetic expression using the account balance."""
    allowed_operators = {
        ast.Add: lambda left, right: left + right,
        ast.Sub: lambda left, right: left - right,
        ast.Mult: lambda left, right: left * right,
        ast.Div: lambda left, right: left / right,
        ast.Pow: lambda left, right: left**right,
        ast.Mod: lambda left, right: left % right,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Name) and node.id == "bal":
            return balance
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = evaluate(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        raise ValueError("Unsupported bonus expression")

    parsed_expression = ast.parse(expression, mode="eval")
    return evaluate(parsed_expression)


def compute_bonus(acc_id, expr):
    """Compute a bonus from a restricted arithmetic expression."""
    if acc_id not in account_data:
        raise KeyError(f"Account {acc_id} does not exist")

    balance = account_data[acc_id]["balance"]
    return _evaluate_bonus_expression(expr, balance)


def get_hash(pin, salt=None):
    """Return a salted PBKDF2-HMAC hash for a PIN."""
    if not isinstance(pin, str) or not pin:
        raise ValueError("PIN must be a non-empty string")

    salt = salt or os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 200_000)
    return f"{salt.hex()}${derived_key.hex()}"


def verify_pin(pin, stored_hash):
    """Verify a PIN against the salted hash returned by get_hash."""
    try:
        salt_hex, expected_hash = stored_hash.split("$", maxsplit=1)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False

    actual_hash = get_hash(pin, salt).split("$", maxsplit=1)[1]
    return hmac.compare_digest(actual_hash, expected_hash)


def generate_temp_pin():
    """Generate a cryptographically secure four-digit temporary PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Write account data to a backup file."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        backup_file.write(repr(account_data))


def main():
    """Run a small demonstration of the bank account functions."""
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))

    pin_hash = get_hash("1234")
    print("PIN verified:", verify_pin("1234", pin_hash))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Backup complete.")


if __name__ == "__main__":
    main()

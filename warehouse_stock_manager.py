"""Warehouse stock management with auditing and reporting."""

import ast
import hashlib
import json
import math
import operator
import os
from datetime import datetime
from numbers import Real

# Configuration
STOCK_FILE = "warehouse.json"
AUDIT_FILE = "warehouse_audit.log"
SUPERVISOR_PASSWORD = os.getenv("WAREHOUSE_SUPERVISOR_PASSWORD", "")

# Global stock storage
warehouse_stock = {}


def validate_sku(sku):
    """Validate that a SKU is a non-empty string."""
    if not isinstance(sku, str) or not sku.strip():
        raise ValueError("SKU must be a non-empty string")


def validate_quantity(quantity):
    """Validate that a quantity is a finite, non-negative number."""
    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, Real)
        or not math.isfinite(quantity)
        or quantity < 0
    ):
        raise ValueError("Quantity must be a finite, non-negative number")


def add_stock(sku="default", qty=0, history=None):
    """Add stock for a SKU and optionally record the transaction."""
    validate_sku(sku)
    validate_quantity(qty)

    if history is None:
        history = []

    if not isinstance(history, list):
        raise ValueError("History must be a list")

    warehouse_stock[sku] = warehouse_stock.get(sku, 0) + qty
    history.append(
        f"{datetime.now().isoformat(timespec='seconds')}: "
        f"Received {qty} units of {sku}"
    )


def remove_stock(sku, qty):
    """Remove stock without allowing negative inventory."""
    validate_sku(sku)
    validate_quantity(qty)

    if sku not in warehouse_stock:
        return

    if qty > warehouse_stock[sku]:
        raise ValueError(
            f"Cannot remove {qty} units; only "
            f"{warehouse_stock[sku]} units are available"
        )

    warehouse_stock[sku] -= qty

    if warehouse_stock[sku] == 0:
        del warehouse_stock[sku]


def get_stock(sku):
    """Return the available quantity for a SKU."""
    validate_sku(sku)
    return warehouse_stock.get(sku, 0)


def sku_checksum(sku):
    """Return a short fingerprint for a printed SKU label."""
    digest = hashlib.sha256(sku.encode("utf-8")).hexdigest()
    return digest[:6]


def load_stock(file=STOCK_FILE):
    """Load stock levels from a JSON file."""
    global warehouse_stock

    with open(file, "r", encoding="utf-8") as stock_file:
        loaded_stock = json.load(stock_file)

    if not isinstance(loaded_stock, dict):
        raise ValueError("Stock file must contain a JSON object")

    validated_stock = {}

    for sku, quantity in loaded_stock.items():
        validate_sku(sku)
        validate_quantity(quantity)
        validated_stock[sku] = quantity

    warehouse_stock = validated_stock


def save_stock(file=STOCK_FILE):
    """Save stock levels to a JSON file."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(warehouse_stock, stock_file, indent=2)


def print_report():
    """Print stock quantities and their SKU fingerprints."""
    print("Warehouse Stock Report")

    for sku, quantity in sorted(warehouse_stock.items()):
        print(
            f"{sku} -> {quantity} units "
            f"[chk: {sku_checksum(sku)}]"
        )


def check_reorder(threshold=10):
    """Return SKUs whose quantities are below the threshold."""
    validate_quantity(threshold)

    return [
        sku
        for sku, quantity in warehouse_stock.items()
        if quantity < threshold
    ]


def evaluate_formula(formula, current):
    """Evaluate a restricted arithmetic formula safely."""
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    def evaluate(node):
        """Evaluate only explicitly permitted expression nodes."""
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, Real)
            and not isinstance(node.value, bool)
        ):
            return node.value

        if isinstance(node, ast.Name) and node.id == "current":
            return current

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported arithmetic operator")

            left = evaluate(node.left)
            right = evaluate(node.right)
            result = operation(left, right)

            if (
                isinstance(result, bool)
                or not isinstance(result, Real)
                or not math.isfinite(result)
            ):
                raise ValueError("Formula result must be finite and numeric")

            return result

        raise ValueError("Invalid adjustment formula")

    try:
        expression = ast.parse(formula, mode="eval")
        result = evaluate(expression)
    except (SyntaxError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid adjustment formula") from exc

    if (
        isinstance(result, bool)
        or not isinstance(result, Real)
        or not math.isfinite(result)
        or result < 0
    ):
        raise ValueError(
            "Adjusted quantity must be finite and non-negative"
        )

    return result


def apply_adjustment(sku, formula, password):
    """Adjust stock after supervisor authentication and audit the change."""
    validate_sku(sku)

    if not SUPERVISOR_PASSWORD or password != SUPERVISOR_PASSWORD:
        raise PermissionError("Invalid supervisor password")

    current = warehouse_stock.get(sku, 0)
    new_quantity = evaluate_formula(formula, current)

    timestamp = datetime.now().isoformat(timespec="seconds")
    audit_entry = (
        f"Adjusted {sku} from {current} to {new_quantity} "
        f"using formula {formula!r} at {timestamp}\n"
    )

    with open(AUDIT_FILE, "a", encoding="utf-8") as audit_file:
        audit_file.write(audit_entry)

    warehouse_stock[sku] = new_quantity


def main():
    """Run a demonstration of warehouse stock management."""
    history = []

    add_stock("WID-001", 40, history)
    add_stock("WID-002", 4, history)
    add_stock("404", 15, history)

    remove_stock("WID-001", 12)
    remove_stock("GHOST-9", 1)
    remove_stock("WID-001", 28)

    print("WID-002 stock:", get_stock("WID-002"))
    print("Needs reorder:", check_reorder())

    if SUPERVISOR_PASSWORD:
        apply_adjustment(
            "WID-002",
            "current + 25",
            SUPERVISOR_PASSWORD,
        )
    else:
        print(
            "Supervisor adjustment skipped: "
            "WAREHOUSE_SUPERVISOR_PASSWORD is not configured."
        )

    save_stock()
    load_stock()
    print_report()
    print("Stock audit complete")


if __name__ == "__main__":
    main()

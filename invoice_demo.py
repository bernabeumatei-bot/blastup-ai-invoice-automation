"""Fictional invoice intake and exception validation; no OCR or ERP connection."""
from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def money(value: object) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError("invalid amount")
    return amount


def validate_invoice(invoice: dict, seen: set[tuple[str, str]]) -> dict:
    """Return an import candidate or a review case with explicit reasons."""
    reasons: list[str] = []
    supplier = str(invoice.get("supplier", "")).strip()
    tax_id = str(invoice.get("supplier_tax_id", "")).strip()
    number = str(invoice.get("invoice_number", "")).strip()
    if not supplier:
        reasons.append("missing_supplier")
    if not tax_id:
        reasons.append("missing_supplier_tax_id")
    if not number:
        reasons.append("missing_invoice_number")
    if invoice.get("currency") != "EUR":
        reasons.append("unsupported_currency")
    try:
        date.fromisoformat(str(invoice.get("invoice_date", "")))
    except ValueError:
        reasons.append("invalid_invoice_date")
    try:
        net = money(invoice.get("net_amount"))
        tax = money(invoice.get("tax_amount"))
        total = money(invoice.get("total_amount"))
        if abs(net + tax - total) > Decimal("0.01"):
            reasons.append("total_mismatch")
    except ValueError:
        reasons.append("invalid_amount")
    if tax_id and number:
        key = (tax_id.casefold(), number.casefold())
        if key in seen:
            reasons.append("possible_duplicate")
        seen.add(key)
    return {
        "invoice_number": number or None,
        "supplier": supplier or None,
        "status": "review" if reasons else "ready_for_reviewed_export",
        "reasons": reasons,
    }


def process_invoices(invoices: list[dict]) -> dict:
    seen: set[tuple[str, str]] = set()
    results = [validate_invoice(invoice, seen) for invoice in invoices]
    return {
        "ready_for_reviewed_export": [item for item in results if not item["reasons"]],
        "exceptions": [item for item in results if item["reasons"]],
        "summary": {
            "received": len(results),
            "ready": sum(not item["reasons"] for item in results),
            "review": sum(bool(item["reasons"]) for item in results),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate fictional invoice records")
    parser.add_argument("input", nargs="?", default="examples/invoices.json")
    args = parser.parse_args()
    invoices = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(invoices, list) or any(not isinstance(item, dict) for item in invoices):
        parser.error("Input must be a JSON array of invoice objects")
    print(json.dumps(process_invoices(invoices), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

import unittest

from invoice_demo import process_invoices


class InvoiceDemoTests(unittest.TestCase):
    def test_flags_mismatch_duplicate_and_missing_tax_id(self):
        base = {
            "supplier": "Empresa Demo",
            "supplier_tax_id": "DEMO-1",
            "invoice_number": "A-1",
            "invoice_date": "2026-01-01",
            "currency": "EUR",
            "net_amount": "100",
            "tax_amount": "21",
            "total_amount": "121",
        }
        mismatch = dict(base, invoice_number="A-2", total_amount="120")
        missing = dict(base, invoice_number="A-3", supplier_tax_id="")
        result = process_invoices([base, base, mismatch, missing])
        self.assertEqual(result["summary"], {"received": 4, "ready": 1, "review": 3})
        self.assertIn("possible_duplicate", result["exceptions"][0]["reasons"])
        self.assertIn("total_mismatch", result["exceptions"][1]["reasons"])
        self.assertIn("missing_supplier_tax_id", result["exceptions"][2]["reasons"])


if __name__ == "__main__":
    unittest.main()

"""Currency formatting helpers."""


def format_currency(amount, symbol="$"):
    return f"{symbol}{amount:,.2f}"

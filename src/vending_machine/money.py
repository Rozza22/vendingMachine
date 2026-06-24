from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

TWOPLACES = Decimal("0.01")


class InvalidMoney(ValueError):
    pass


def parse_money(value) -> Decimal:
    if isinstance(value, Decimal):
        d = value
    elif isinstance(value, int):
        d = Decimal(value)
    elif isinstance(value, float):
        d = Decimal(str(value))
    elif isinstance(value, str):
        s = value.strip()
        if not s:
            raise InvalidMoney("Empty money string")
        try:
            d = Decimal(s)
        except InvalidOperation:
            raise InvalidMoney(f"Invalid monetary value: {value!r}")
    else:
        raise TypeError(f"Unsupported type for money: {type(value).__name__}")

    try:
        d = d.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        raise InvalidMoney(f"Cannot normalize monetary value: {value!r}")

    if d < 0:
        raise InvalidMoney(f"Negative monetary value not allowed: {d}")

    return d

from __future__ import annotations

import math

from fastmcp import FastMCP


mcp = FastMCP("Basic Math Server")

Number = int | float | str


def _as_number(value: Number) -> float:
    """Convert a number or numeric string to a finite float."""
    if isinstance(value, bool):
        raise TypeError("Expected a number, not a boolean")

    try:
        number = float(value.strip()) if isinstance(value, str) else float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Expected a number (int, float, or numeric string)"
        ) from exc

    if not math.isfinite(number):
        raise ValueError("The number must be finite")
    return number


@mcp.tool()
async def add(a: Number, b: Number) -> float:
    """Add two numbers and return a + b."""
    return _as_number(a) + _as_number(b)


@mcp.tool()
async def subtract(a: Number, b: Number) -> float:
    """Subtract b from a and return a - b."""
    return _as_number(a) - _as_number(b)


@mcp.tool()
async def multiply(a: Number, b: Number) -> float:
    """Multiply two numbers and return a * b."""
    return _as_number(a) * _as_number(b)


@mcp.tool()
async def divide(a: Number, b: Number) -> float:
    """Divide a by b."""
    divisor = _as_number(b)
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return _as_number(a) / divisor


@mcp.tool()
async def floor_divide(a: Number, b: Number) -> float:
    """Floor-divide a by b and return a // b."""
    divisor = _as_number(b)
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return _as_number(a) // divisor


@mcp.tool()
async def modulo(a: Number, b: Number) -> float:
    """Return the remainder of a divided by b."""
    divisor = _as_number(b)
    if divisor == 0:
        raise ValueError("Cannot calculate modulo zero")
    return _as_number(a) % divisor


@mcp.tool()
async def power(base: Number, exponent: Number) -> float:
    """Raise base to exponent."""
    result = _as_number(base) ** _as_number(exponent)
    if isinstance(result, complex):
        raise ValueError("This operation produces a complex number")
    if not math.isfinite(result):
        raise ValueError("The result is too large or is not finite")
    return result


@mcp.tool()
async def square_root(value: Number) -> float:
    """Return the non-negative square root of a number."""
    number = _as_number(value)
    if number < 0:
        raise ValueError("Cannot calculate the square root of a negative number")
    return math.sqrt(number)


@mcp.tool()
async def absolute(value: Number) -> float:
    """Return the absolute value of a number."""
    return abs(_as_number(value))


@mcp.tool()
async def percentage(value: Number, percent: Number) -> float:
    """Calculate percent percent of value."""
    return _as_number(value) * _as_number(percent) / 100


@mcp.tool()
async def factorial(value: int) -> int:
    """Return the factorial of a non-negative integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("Factorial requires an integer")
    if value < 0:
        raise ValueError("Factorial requires a non-negative integer")
    return math.factorial(value)


if __name__ == "__main__":
    mcp.run()

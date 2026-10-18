"""Dependency-free helpers for exact SDSS object identifiers."""

from numbers import Integral


def exact_objid(value: object) -> str:
    """
    Convert an exact SDSS object identifier to a decimal string.

    Accepted:
        - Python integers
        - NumPy integer scalars
        - Decimal digit strings

    Rejected:
        - Floats, including integer-valued floats
        - Scientific notation
        - Null values
        - Booleans
        - Invalid or negative identifiers

    A floating-point identifier cannot be trusted because
    conversion may already have destroyed integer precision.
    """

    if isinstance(value, bool):
        raise TypeError(
            "Boolean values are not valid SDSS identifiers."
        )

    if isinstance(value, Integral):
        identifier = str(value)

    elif isinstance(value, str):
        identifier = value.strip()

    else:
        raise TypeError(
            "SDSS identifier has an unsafe data type: "
            f"{type(value).__name__}. "
            "Expected an exact integer or decimal string."
        )

    if not identifier:
        raise ValueError(
            "SDSS identifier is empty."
        )

    if not (
        identifier.isascii()
        and identifier.isdecimal()
    ):
        raise ValueError(
            "SDSS identifier must contain decimal digits only."
        )

    return identifier

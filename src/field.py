from dataclasses import dataclass


@dataclass
class Field:
    """
    A hollerith Field

    Used when writing tables in `write_table` to format columns
    in a fixed width line.

    Parameters
    ----------
    type : type
        The type of the field. This could be one of
        `None`, `str`, `int`, or `float`.
    width: int
        The width of the field in characters.

    """

    type: type = None
    width: int = None

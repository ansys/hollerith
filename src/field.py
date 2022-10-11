from dataclasses import dataclass


@dataclass
class Field:
    type: type = None
    width: int = None

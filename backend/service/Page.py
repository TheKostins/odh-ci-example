from dataclasses import dataclass

@dataclass
class Page[T]:
    limit: int
    offset: int
    total: int
    items: list[T]

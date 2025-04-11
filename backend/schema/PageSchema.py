from typing import Callable
from pydantic import BaseModel

from service.Page import Page

class PageSchema[T](BaseModel):
    limit: int
    offset: int
    total: int
    items: list[T]


def create_page_schema_from_page[T, E](page: Page[T], item_converter: Callable[[T], E]) -> PageSchema[E]:
    items_schema = [item_converter(item) for item in page.items]
    return PageSchema[E](
        limit=page.limit,
        offset=page.offset,
        total=page.total,
        items=items_schema
    )

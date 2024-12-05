from typing import List, Optional

from app.config.enums.repository import InFilterType
from app.interfaces import CustomBaseModel


class InFilters(CustomBaseModel):
    filter_key: str
    filter_values: List
    type: InFilterType


class RepositoryInFilters(CustomBaseModel):
    filters: List[InFilters]


class BetweenFilters(CustomBaseModel):
    filter_key: str
    filter_start: str
    filter_end: str


class RepositoryBetweenFilters(CustomBaseModel):
    filters: List[BetweenFilters]


class RepositoryPagination(CustomBaseModel):
    current_page: Optional[int] = 1
    items_per_page: Optional[int] = 30


class RepositoryPaginationResponse(RepositoryPagination):
    current_page: Optional[int]
    next_page: Optional[int]
    previous_page: Optional[int]
    total_items: Optional[int]
    total_pages: Optional[int]
    items: Optional[List[CustomBaseModel]]


class RepositoryUpsert(CustomBaseModel):
    origin: Optional[str] = "System"
    find_key: Optional[str]
    find_key_value: Optional[int | str]
    find_key_value_str: Optional[str]
    values_to_upsert: dict
    with_deleteds: Optional[bool] = False
    upsert_many: Optional[bool] = False


class RepositoryDeletion(CustomBaseModel):
    find_key: str
    find_key_value: Optional[int | str]
    modify_many: Optional[bool] = False


class RepositoryLikeSearch(CustomBaseModel):
    field_name: Optional[str]
    field_value: Optional[str]

from ..exceptions import FieldError as FieldError
from .base import ResourceModel as ResourceModel
from typing import Any, List

class Event(ResourceModel):
    pass

class Webhook(ResourceModel):
    EVENTS: Any = ...
    RESOURCE: str = ...

    events: List[str]
    method: str
    description: str
    url: str
    def init_custom_fields(
        self, method: Any = ..., events: Any = ..., **kwargs: Any
    ) -> None: ...
    def validate_custom_fields(self, **kwargs: Any): ...
    def get_original_different_fields_mapping(self): ...
    @classmethod
    def get_required_fields(cls: Any) -> set: ...
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

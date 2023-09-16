from __future__ import annotations

from typing import Any, TypeVar

from django.db.models import Model

ModelT = TypeVar("ModelT", bound=Model)

def get_object_or_none(model: type[ModelT], **kwargs: Any) -> ModelT | None:
    try:
        return model.objects.get(**kwargs)  # type: ignore[attr-defined]
    except model.DoesNotExist:  # type: ignore[attr-defined]
        return None

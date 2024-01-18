import json
from typing import Optional, Union

import pydantic
from aiohttp import web

from server import get_http_error


class CheckCreateAdvert(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.validator("title")
    @classmethod
    def check_title(cls, value):
        if len(value) > 30:
            raise ValueError("title must be less than 30 chars")
        return value

    @pydantic.validator("description")
    @classmethod
    def check_description(cls, value):
        if len(value) > 200:
            raise ValueError("description must be less than 200 chars")
        return value

    @pydantic.validator("owner")
    @classmethod
    def check_owner(cls, value):
        if len(value) > 30:
            raise ValueError("owner_name must be less than 30 chars")
        return value


class CheckUpdateAdvert(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @pydantic.validator("title")
    @classmethod
    def check_title(cls, value):
        if len(value) > 30:
            raise ValueError("title must be less than 30 chars")
        return value

    @pydantic.validator("description")
    @classmethod
    def check_description(cls, value):
        if len(value) > 200:
            raise ValueError("description must be less than 200 chars")
        return value

    @pydantic.validator("owner")
    @classmethod
    def check_owner(cls, value):
        if len(value) > 30:
            raise ValueError("owner_name must be less than 30 chars")
        return value


def validate(check_class, data: dict):
    try:
        data_validated = check_class(**data).dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise get_http_error(error_class=web.HTTPBadRequest, message=er.errors())
    return data_validated

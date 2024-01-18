import json
from typing import Optional, Union

import pydantic
from aiohttp import web

# class HttpError(web.HTTPException):
#     def __init__(self, error_message: Union[str, dict, list]):
#         message = json.dumps({"status": "error", "description": error_message})
#         super().__init__(text=message, content_type="application/json")
#
#
# class BadRequest(HttpError):
#     status_code = 400


class CheckCreateAdvert(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.validator("title")
    def check_title(cls, value):
        if len(value) > 30:
            raise ValueError("title must be less than 30 chars")
        return value

    @pydantic.validator("description")
    def check_description(cls, value):
        if len(value) > 200:
            raise ValueError("description must be less than 200 chars")
        return value

    @pydantic.validator("owner")
    def check_owner(cls, value):
        if len(value) > 30:
            raise ValueError("owner_name must be less than 30 chars")
        return value


class CheckUpdateAdvert(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    owner: Optional[str]

    @pydantic.validator("title")
    def check_title(cls, value):
        if len(value) > 30:
            raise ValueError("title must be less than 30 chars")
        return value

    @pydantic.validator("description")
    def check_description(cls, value):
        if len(value) > 200:
            raise ValueError("description must be less than 200 chars")
        return value

    @pydantic.validator("owner")
    def check_owner(cls, value):
        if len(value) > 30:
            raise ValueError("owner_name must be less than 30 chars")
        return value


def validate(check_class, data: dict):
    try:
        data_validated = check_class(**data).dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise BadRequest(er.errors())
    return data_validated

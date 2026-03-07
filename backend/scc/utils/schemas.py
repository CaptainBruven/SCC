from typing import TypeVar

from ninja import Field, Schema
from pydantic import BaseModel

from scc.utils.error_codes import ErrorCodes

DataT = TypeVar("DataT")


class ResponseSchema[DataT](BaseModel):
    error: bool = False
    code: str | None = None
    message: str | None = None
    data: DataT | None = None


class ErrorSchema[DataT](Schema):
    code: str = Field(ErrorCodes.UNKNOWN_ERROR)
    error: bool = Field(True)
    message: str | None = None
    data: DataT | None = None

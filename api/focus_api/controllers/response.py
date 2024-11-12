from typing import Any, Optional, Type, Union

from flask import request
from werkzeug.exceptions import (
    BadRequest,
    Conflict,
    Forbidden,
    HTTPException,
    NotFound,
    ServiceUnavailable,
)

from opr_api.utils.pydantic import PydanticBaseModel


class ValidationErrorDetail(PydanticBaseModel):
    type: str
    message: str = ""
    field: Optional[str] = None
    value: Optional[str] = None
    extra: Optional[dict[str, str]] = None


class PagingMetaData(PydanticBaseModel):
    page_offset: int
    page_size: int
    total_records: int
    total_pages: int
    order_by: str
    order_direction: str


class MetaData(PydanticBaseModel):
    resource: str
    method: str
    query: Optional[dict[str, str]] = None
    paging: Optional[PagingMetaData] = None


class Response(PydanticBaseModel):
    status_code: int
    message: str = ""
    meta: Optional[MetaData] = None
    data: Union[None, dict, list[dict]] = None
    warnings: Optional[list[ValidationErrorDetail]] = None
    errors: Optional[list[ValidationErrorDetail]] = None

    def to_api_response(self) -> tuple[dict[str, Any], int, dict[str, str]]:
        if self.meta is None:
            self.meta = MetaData(method=request.method, resource=request.path)
        else:
            self.meta.method = request.method
            self.meta.method = request.path

        return (
            self.model_dump(exclude_none=True, by_alias=True),
            200,
            {"Content-Type": "application/json"},
        )


def success_response(
    message: str,
    data: Union[None, dict, list[dict]] = None,
    warnings: Optional[list[ValidationErrorDetail]] = None,
    status_code: int = 200,
    meta: Optional[MetaData] = None,
) -> Response:
    return Response(
        status_code=status_code, message=message, data=data, warnings=warnings, meta=meta
    )


def error_response(
    status_code: Union[
        HTTPException,
        Type[HTTPException],
        Type[BadRequest],
        Type[Conflict],
        Type[ServiceUnavailable],
        Type[NotFound],
        Type[Forbidden],
    ],
    message: str,
    errors: list[ValidationErrorDetail],
    data: Union[None, dict, list[dict]] = None,
    warnings: Optional[list[ValidationErrorDetail]] = None,
) -> Response:
    code = status_code.code if status_code.code is not None else 400

    return Response(status_code=code, message=message, errors=errors, data=data, warnings=warnings)

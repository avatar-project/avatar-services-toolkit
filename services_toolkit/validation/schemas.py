from logging import getLogger

from marshmallow import Schema, fields, validate

logger = getLogger(__name__)


class ResponseSchema(Schema):
    headers = fields.Dict(required=False, allow_none=False, default=dict())
    message = fields.Str(required=True, allow_none=True, default='')
    result = fields.Dict(required=True, allow_none=True)
    success = fields.Bool(required=True, allow_none=False)


class SuccessResponseSchema(ResponseSchema):
    success = fields.Bool(required=True, allow_none=False, validate=validate.Equal(True), default=True)


class ErrorResponseSchema(ResponseSchema):
    success = fields.Bool(required=True, allow_none=False, validate=validate.Equal(False), default=False)

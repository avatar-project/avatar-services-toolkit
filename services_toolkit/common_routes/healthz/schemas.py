from marshmallow import Schema, fields


class RootResponseSchema(Schema):
    name = fields.Str(required=True, allow_none=False)
    version = fields.Str(required=False, allow_none=True, default=None)

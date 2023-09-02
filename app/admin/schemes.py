from marshmallow import Schema, fields


class AdminSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str()


class AdminResponseSchema(Schema):
    id = fields.Int()
    email = fields.Str()

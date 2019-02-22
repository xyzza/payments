from marshmallow import Schema
from marshmallow import fields


class ReportSchema(Schema):
    op_type = fields.Boolean()
    timestamp = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    balance = fields.Str()
    id = fields.Str()
    amoun = fields.Str()
    status = fields.Str()


report_schema = ReportSchema()

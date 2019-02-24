from marshmallow import Schema
from marshmallow import fields


class ReportInputSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    begin = fields.DateTime('%Y-%m-%d %H:%M:%S.%f')
    end = fields.DateTime('%Y-%m-%d %H:%M:%S.%f')
    csv = fields.Bool()


class ReportOutputSchema(Schema):
    timestamp = fields.Str()
    sender_id = fields.Int()
    from_user = fields.Str()
    op_type = fields.Str()
    amount = fields.Str()
    recipient_id = fields.Int()
    to_user = fields.Str()
    status = fields.Str()
    sender_balance = fields.Str()
    recipient_balance = fields.Str()


_input_schema = ReportInputSchema()
_output_schema = ReportOutputSchema()

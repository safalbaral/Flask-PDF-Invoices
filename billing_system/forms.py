from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField
from wtforms.fields import DateField
from wtforms.validators import InputRequired, NumberRange
from billing_system import app


class AdditionalItemsForm(Form):
    item_description = StringField('Description')

    price = IntegerField('Price', default=0, validators=[
        NumberRange(min=0),
        InputRequired()
    ])

    quantity = IntegerField('Quantity', default=0, validators=[
        NumberRange(min=0),
        InputRequired()
    ])

    def __init__(self, *args, **kwargs):
        super(AdditionalItemsForm, self).__init__(
            meta={'csrf': False}, *args, **kwargs)

class ProcessCheckOutForm(FlaskForm):
    additional_items = FieldList(FormField(AdditionalItemsForm), min_entries=20)

    discount_percent = IntegerField('Discount Percent', default=0, validators=[
        NumberRange(min=0, max=100)
    ])

    guest_name = StringField('Invoice To:', validators=[
        InputRequired()
    ])
    invoice_id = IntegerField('Invoice ID:', validators=[
        InputRequired()
    ])

    submit = SubmitField('Complete Check Out')

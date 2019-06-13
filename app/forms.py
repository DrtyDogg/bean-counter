from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    amount = DecimalField('Amount',
                          validators=[DataRequired(
                              message='Amount is required')],
                          places=2)
    location = StringField('Purchase location',
                           validators=[DataRequired()])
    date = DateField('Date of purchase',
                     validators=[DataRequired()],
                     format='%m/%d/%Y')
    description = StringField('Description')
    submit = SubmitField('Save transaction')


class CategoryForm(FlaskForm):
    title = StringField('Category name',
                        validators=[DataRequired()])
    budget_amount = DecimalField('Budgeted amount',
                                 validators=[DataRequired()],
                                 places=2)
    submit = SubmitField('Save')

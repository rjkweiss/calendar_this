from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired


class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('StartDate', validators=[DataRequired()], format="%Y-%m-%d")
    start_time = TimeField('StartTime', validators=[DataRequired()], format="%H:%M")
    end_date = DateField('EndDate', validators=[DataRequired()], format="%Y-%m-%d")
    end_time = TimeField('EndTime', validators=[DataRequired()], format="%H:%M")
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField('Schedule Appointment')

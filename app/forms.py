from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, ValidationError


class AppointmentForm(FlaskForm):
    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)

        if start >= end:
            msg = 'End date/time must come after start date/time'
            raise ValidationError(msg)

    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('StartDate', validators=[DataRequired()], format="%Y-%m-%d")
    start_time = TimeField('StartTime', validators=[DataRequired()], format="%H:%M")
    end_date = DateField('EndDate', validators=[DataRequired()], format="%Y-%m-%d")
    end_time = TimeField('EndTime', validators=[DataRequired()], format="%H:%M")
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private')
    submit = SubmitField('Schedule Appointment')

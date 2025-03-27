import os
from datetime import datetime, timedelta

import psycopg2
from flask import Blueprint, redirect, render_template, url_for

from app.forms import AppointmentForm

bp = Blueprint('main', __name__, '/')

CONNECTION_PARAMETERS = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'dbname': os.environ.get('DB_NAME'),
    'host': os.environ.get('DB_HOST')
}

# display the appointments for a given day
@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily(year, month, day):
    # instantiate the form
    form = AppointmentForm()

    # handle form submission
    if form.validate_on_submit():
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
            'description': form.description.data,
            'private': form.private.data
        }

        # create a new record to the database
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                curs.execute("""
                    INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
                    VALUES(%(name)s,%(start_datetime)s,%(end_datetime)s,%(description)s,%(private)s)
                    """,
                    params
                )

        # redirect to '/'
        return redirect('/')

    selected_day = datetime(year, month, day)
    next_day = selected_day + timedelta(days=1)


    # establish database connection
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                WHERE start_datetime BETWEEN %(selected_day)s AND %(next_day)s
                ORDER BY start_datetime;
                """,
                {
                    'selected_day': selected_day,
                    'next_day': next_day
                }
            )
            rows = curs.fetchall()

            return render_template('main.html', rows=rows, form=form)


# display main page
@bp.route("/", methods=['GET', 'POST'])
def main():
    curr_date = datetime.now()
    return redirect(url_for(".daily", year=curr_date.year, month=curr_date.month, day=curr_date.day))

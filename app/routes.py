import os
from datetime import datetime

import psycopg2
from flask import Blueprint, redirect, render_template

from app.forms import AppointmentForm

bp = Blueprint('main', __name__, '/')

CONNECTION_PARAMETERS = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'dbname': os.environ.get('DB_NAME'),
    'host': os.environ.get('DB_HOST')
}

# display main page
@bp.route("/", methods=['GET', 'POST'])
def main():
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


    # establish database connection
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                ORDER BY start_datetime;
                """
            )
            rows = curs.fetchall()

            return render_template('main.html', rows=rows, form=form)

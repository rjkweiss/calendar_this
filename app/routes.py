from flask import Blueprint, render_template

bp = Blueprint('main', __name__, '/')

# display main page
@bp.route("/")
def main():
    return render_template('main.html')

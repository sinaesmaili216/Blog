from flask import render_template, Blueprint

from countries.auth import login_required
from countries.db import get_db

bp = Blueprint("info", __name__)




@bp.route('/')
@login_required
def home():
    db = get_db()
    countries = db.execute("SELECT * FROM country").fetchall()
    return render_template('index.html', countries=countries)


@bp.route('/country/<int:country_id>')
@login_required
def country(country_id):
    country_data = get_db().execute("SELECT * FROM country WHERE id = ?", (country_id,)).fetchone()
    return render_template('country.html', country=country_data)

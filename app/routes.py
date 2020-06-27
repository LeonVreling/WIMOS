from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_user import current_user, login_required

from app import app
from app.models import *
from app.forms import *


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    return render_template('resolutions.html', resolutions=Resolution.query.all())


@app.route('/moties/<id>')
@login_required
def resolution(id):
    pass


@app.route('/moties/indienen', methods=['GET', 'POST'])
@login_required
def submit_resolution():
    form = ResolutionForm()
    print(form.errors)
    if form.validate_on_submit():
        res = Resolution(observation=form.observation.data, consideration=form.consideration.data,
                         decision=form.decision.data, user_id=current_user.id, alcohol=form.alcohol.data,
                         timestamp=datetime.now())
        db.session.add(res)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('resolutionform.html', form=form)
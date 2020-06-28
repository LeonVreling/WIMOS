from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_user import current_user, login_required, roles_required

from app import app, user_manager
from app.models import *
from app.forms import *


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    resolutions = Resolution.query.all()

    return render_template('resolutions.html', resolutions=resolutions, Vote=Vote, Seen=Seen)


@app.route('/moties/<id>')
@login_required
def resolution(id):
    pass


@app.route('/moties/<id>/voor')
@roles_required('Voorzitter')
def vote_resolution(id):
    res = Resolution.query.get(id)
    vote = Vote(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
    db.session.add(vote)
    db.session.commit()
    mark_resolution_as_seen(id)
    return redirect(url_for('index'))


@app.route('/moties/<id>/gezien')
@roles_required('Voorzitter')
def mark_resolution_as_seen(id):
    res = Resolution.query.get(id)
    seen = Seen(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
    db.session.add(seen)
    db.session.commit()
    return redirect(url_for('index'))


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


@app.route('/leden/toevoegen', methods=['GET', 'POST'])
@login_required
@roles_required('Voorzitter')
def register_board_member():
    form = RegisterForm()
    if form.validate_on_submit():
        password = user_manager.password_manager.hash_password(form.password.data)
        user = User(username=form.username.data, password=password, association=current_user.association)
        db.session.add(user)
        db.session.commit()

        user_manager.db_manager.add_user_role(user, form.role.data)
        user_manager.db_manager.commit()

        return redirect(url_for('index'))

    return render_template('register_board_member.html', form=form)
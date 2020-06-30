from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_user import current_user, login_required, roles_required
from sqlalchemy.exc import IntegrityError

from app import app, user_manager
from app.models import *
from app.forms import *
import app.forms as f


@app.route('/')
def index():
    # If no user is logged in, serve the default html page
    if not current_user.is_authenticated or current_user.is_anonymous:
        return render_template('index.html')

    # Return the resolutions page
    resolutions = Resolution.query.all()
    return render_template('resolutions.html', resolutions=resolutions, Vote=Vote, Seen=Seen)


# Endpoint to vote in favour of a resolution
@app.route('/moties/<id>/voor')
# Can only be done by chairmen
@roles_required('Voorzitter')
def vote_resolution(id):
    res = Resolution.query.get(id)
    vote = Vote(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
    db.session.add(vote)
    db.session.commit()
    # When you vote in favour of a resolution, you have also seen the resolution, so this is marked as well
    try:
        mark_resolution_as_seen(id)
    except IntegrityError:
        pass
    return redirect(url_for('index'))


# Endpoint to mark a resolution as seen
@app.route('/moties/<id>/gezien')
# Can only be done by chairmen
@roles_required('Voorzitter')
def mark_resolution_as_seen(id):
    res = Resolution.query.get(id)
    seen = Seen(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
    db.session.add(seen)
    db.session.commit()
    return redirect(url_for('index'))


# Page/form to hand in resolutions
@app.route('/moties/indienen', methods=['GET', 'POST'])
# Can only be done by board members (no kandies allowed!)
@roles_required('Bestuurslid', 'Voorzitter')
def submit_resolution():
    # Get the form
    form = ResolutionForm()
    if form.validate_on_submit():
        res = Resolution(observation=form.observation.data, consideration=form.consideration.data,
                         decision=form.decision.data, user_id=current_user.id,
                         alcohol=form.before_alcohol.data or f.alcohol_passed, timestamp=datetime.now())
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
        # Hash the password
        password = user_manager.password_manager.hash_password(form.password.data)
        # The new board member is of the same association as the chairman, so we save it as such
        user = User(username=form.username.data, password=password, association=current_user.association)
        db.session.add(user)
        db.session.commit()

        # Give the new user the role as assigned by the chairman (either board member or kandi)
        user_manager.db_manager.add_user_role(user, form.role.data)
        user_manager.db_manager.commit()

        flash("Succesvol {} {} toegevoegd. Hij/zij kan nu inloggen".format(form.role.data, user.username))
        return redirect(url_for('index'))

    return render_template('register_board_member.html', form=form)


@app.route('/admin')
@roles_required('Admin')
def admin():
    print(f.alcohol_passed)
    return render_template('admin.html', alcohol_passed=f.alcohol_passed)


@app.route('/admin/alcohol')
@roles_required('Admin')
def tog_alcohol():
    toggle_alcohol()
    return redirect(url_for('admin'))

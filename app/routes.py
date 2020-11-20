from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_user import current_user, login_required, roles_required
from sqlalchemy.exc import IntegrityError

from app import app, user_manager
from app.models import *
from app.forms import *
import app.forms as f


location = 'Teams (wat betekent Groepen)'
starting_number = 0


@app.route('/')
def index():
    # If no user is logged in, serve the default html page
    if not current_user.is_authenticated or current_user.is_anonymous:
        return render_template('index.html')

    # Return the resolutions page
    return render_template('resolutions.html', Resolution=Resolution, Vote=Vote, Seen=Seen, time=datetime.now(),
                           location=location, starting_number=starting_number)


# Endpoint to vote in favour of a resolution
@app.route('/moties/<id>/voor')
# Can only be done by chairmen
@roles_required('Voorzitter')
def vote_resolution(id):
    res = Resolution.query.get(id)
    if res.passed is not None:
        return redirect(url_for('index'))
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
    if res.passed is not None:
        return redirect(url_for('index'))
    seen = Seen(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
    db.session.add(seen)
    db.session.commit()
    return redirect(url_for('index'))


# Page/form to hand in resolutions
@app.route('/moties/indienen', methods=['GET', 'POST'])
# Can only be done by board members (no kandies allowed!)
@roles_required('Bestuurslid')
def submit_resolution():
    # Get the form
    form = ResolutionForm()
    if form.validate_on_submit():
        res = Resolution(observation=form.observation.data, consideration=form.consideration.data,
                         decision=form.decision.data, user_id=current_user.id,
                         alcohol=form.before_alcohol.data or f.alcohol_passed, timestamp=datetime.now())
        db.session.add(res)
        db.session.commit()
        # seen = Seen(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
        # db.session.add(seen)
        # vote = Vote(resolution_id=res.id, association=current_user.association, timestamp=datetime.now())
        # db.session.add(vote)
        # db.session.commit()
        return redirect(url_for('index'))

    return render_template('resolutionform.html', form=form, location=location)


@app.route('/moties/<id>/goedkeuren')
@roles_required('Organisator')
def pass_resolution(id):
    res = Resolution.query.get(id)
    res.passed = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/moties/<id>/afkeuren')
@roles_required('Organisator')
def reject_resolution(id):
    res = Resolution.query.get(id)
    res.passed = False
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/moties/<id>/ongedaan')
@roles_required('Organisator')
def undo_resolution_vote(id):
    res = Resolution.query.get(id)
    res.passed = None
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/leden/toevoegen', methods=['GET', 'POST'])
@roles_required('Voorzitter')
def register_board_member():
    form = RegisterBoardMemberForm()
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

        flash("Succesvol {} {} toegevoegd. Hij/zij kan nu inloggen".format(form.role.data, user.username), 'success')
        return redirect(url_for('index'))

    return render_template('register_board_member.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
@roles_required('Organisator')
def admin():
    global location, starting_number

    chairman_form = RegisterChairmanForm()
    variable_form = LocationAndStartingNumberForm()

    if chairman_form.submit.data and chairman_form.validate_on_submit():
        # Hash the password
        password = user_manager.password_manager.hash_password(chairman_form.password.data)
        # The new board member is of the same association as the chairman, so we save it as such
        user = User(username=chairman_form.username.data, password=password, association=chairman_form.association.data)
        db.session.add(user)
        db.session.commit()

        # Give the new user the role as assigned by the chairman (either board member or kandi)
        user_manager.db_manager.add_user_role(user, 'Voorzitter')
        user_manager.db_manager.add_user_role(user, 'Bestuurslid')
        user_manager.db_manager.commit()

        flash("Succesvol {} van {} toegevoegd. Hij/zij kan nu inloggen".format(user.username, chairman_form.association.data), 'success')

    if variable_form.submit.data and variable_form.validate_on_submit():
        location = variable_form.location.data
        starting_number = variable_form.starting_number.data

        flash("Succesvol locatie en eerste motienummer aangepast", 'success')

    users = User.query.order_by(User.association).all()
    return render_template('admin.html', alcohol_passed=f.alcohol_passed, chairman_form=chairman_form,
                           variable_form=variable_form, User=User, users=users, location=location,
                           starting_number=starting_number)


@app.route('/admin/alcohol')
@roles_required('Organisator')
def tog_alcohol():
    toggle_alcohol()
    return redirect(url_for('admin'))


@app.route('/admin/gebruiker/verwijderen/<id>')
@roles_required('Organisator')
def admin_delete_user(id):
    user = User.query.get(id)
    resolutions = Resolution.query.filter(Resolution.user_id == id).all()
    if user.has_roles('Admin'):
        flash('Gebruiker {} is een administrator en kan niet verwijderd worden'.format(user.username), 'danger')
    elif len(resolutions) > 0:
        flash('Gebruiker {} kan niet verwijderd worden, omdat hij/zij moties heeft ingediend'.format(user.username),
              'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Gebruiker {} succesvol verwijderd'.format(user.username), 'success')
    return redirect(url_for('admin'))


@app.route('/admin/moties/verwijderen')
@roles_required('Admin')
def admin_delete_all_resolutions():
    Vote.query.delete()
    Seen.query.delete()
    Resolution.query.delete()
    db.session.commit()
    flash('Alle moties succesvol verwijderd', 'success')
    return redirect(url_for('admin'))

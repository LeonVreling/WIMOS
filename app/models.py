from sqlalchemy import select
from sqlalchemy.orm import column_property

from app import db
from flask_user import UserMixin


def vote_to_association(vote):
    return vote.association


# 1 --> Admin
# 2 --> Organisator
# 3 --> Voorzitter
# 4 --> Bestuurslid
# 5 --> Kandi
class Role(db.Model):
    # ID of the Role
    id = db.Column(db.Integer(), primary_key=True)
    # Name of the role (see above)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<'{}'>".format(self.name)


class User(db.Model, UserMixin):
    # ID of the user
    id = db.Column(db.Integer(), primary_key=True)
    # Username of the user
    username = db.Column(db.String(64), index=True, unique=True)
    # Hashed password of the user
    password = db.Column(db.String(128))
    # Whether the account is active and can be used
    active = db.Column(db.Boolean(), default=True)
    # Email address of the user (not used)
    email = db.Column(db.String(128), unique=True)
    # Roles that this user has
    roles = db.relationship('Role', secondary='user_roles')
    # Association this user is a member of
    association = db.Column(db.String(32))


# Mapping from users to roles
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class Vote(db.Model):
    # ID of the resolution
    resolution_id = db.Column(db.Integer(), db.ForeignKey('resolution.id'), primary_key=True)
    # Name of association who voted in favour
    association = db.Column(db.String(), primary_key=True)
    # Time and date of this vote
    timestamp = db.Column(db.DateTime())


class Seen(db.Model):
    # ID of the resolution
    resolution_id = db.Column(db.Integer(), db.ForeignKey('resolution.id'), primary_key=True)
    # Name of association who marked the resolution as seen
    association = db.Column(db.String(), primary_key=True)
    # Time and date of this seen
    timestamp = db.Column(db.DateTime())


class Resolution(db.Model):
    # ID of the resolution
    id = db.Column(db.Integer(), primary_key=True)
    # First part
    observation = db.Column(db.String(512), nullable=False)
    # Second part
    consideration = db.Column(db.String(512), nullable=False)
    # Third part
    decision = db.Column(db.String(512), nullable=False)
    # ID of the user who handed in this resolution
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # Time and date at which this resolution has been handed in
    timestamp = db.Column(db.DateTime())
    # Whether this resolution has passed. None if it has not been decided on yet
    passed = db.Column(db.Boolean())
    # Whether this resolution should be voted on before or after the "alcoholstreep"
    alcohol = db.Column(db.Boolean())
    # Records of votes
    votes = db.relationship('Vote', backref='resolution', lazy='dynamic')
    # Records of seen
    seen_by = db.relationship('Seen', backref='resolution', lazy='dynamic')

    association = column_property(select([User.association]).where(User.id == user_id))

    # Parse the vote objects into a list of strings (association names)
    def vote_list(self):
        return list(map(vote_to_association, self.votes))

    # Parse the seen objects into a list of strings (association names)
    def seen_list(self):
        return list(map(vote_to_association, self.seen_by))

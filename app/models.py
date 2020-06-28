from app import db
from flask_user import UserMixin


# 1 --> Admin
# 2 --> Organisator
# 3 --> Voorzitter
# 4 --> Bestuurslid
# 5 --> Kandi
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<'{}'>".format(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=True)
    email = db.Column(db.String(128), unique=True)
    roles = db.relationship('Role', secondary='user_roles')
    association = db.Column(db.String(32))


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class Resolution(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    observation = db.Column(db.String(512), nullable=False)
    consideration = db.Column(db.String(512), nullable=False)
    decision = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime())
    passed = db.Column(db.Boolean())
    alcohol = db.Column(db.Boolean())


class Vote(db.Model):
    resolution_id = db.Column(db.Integer(), db.ForeignKey('resolution.id'), primary_key=True)
    association = db.Column(db.String(), primary_key=True)
    timestamp = db.Column(db.DateTime())

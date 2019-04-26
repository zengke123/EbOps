from . import db
from flask_login import UserMixin
from . import login_manager



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=2)
    status = db.Column(db.SmallInteger, default=0)


    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
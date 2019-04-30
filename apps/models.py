from . import db
from flask_login import UserMixin
from . import login_manager



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    mail = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default=2)
    status = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)


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


# 作业计划项目
class OpsItem(db.Model):
    __tablename__ = 'ops_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(64), index=True, unique=True)
    c_name = db.Column(db.String(64), unique=True)


# 作业计划明细
class OpsInfo(db.Model):
    __tablename__ = 'ops_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(64), index=True)
    item_id = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)
    cycle = db.Column(db.String(64))


# 作业计划明细
class OpsResult(db.Model):
    __tablename__ = 'ops_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.String(64), index=True)
    date = db.Column(db.DATE, index=True)
    time = db.Column(db.Time, index=True)
    s_times = db.Column(db.SmallInteger, default=0)
    f_times = db.Column(db.SmallInteger, default=0)
    result = db.Column(db.String(255))
    log_id = db.Column(db.String(64))


# 例检主机
class CheckHost(db.Model):
    __tablename__ = 'c_host'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node = db.Column(db.String(32), index=True, nullable=False)
    cluster = db.Column(db.String(32), index=True, nullable=False)
    hostname = db.Column(db.String(32), unique=True, nullable=False)


# 例检历史记录
class CheckHistory(db.Model):
    __tablename__ = 'c_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checktime = db.Column(db.String(64), nullable=False)
    hostname = db.Column(db.String(32), index=True, nullable=False)
    type = db.Column(db.String(32), nullable=False)
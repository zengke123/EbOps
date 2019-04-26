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


# 作业计划项目
class OpsItem(db.Model):
    __tablename__ = 'ops_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(64), index=True, unique=True)
    c_name = db.Column(db.String(64), unique=True)


# IMS作业计划明细
class OpsInfoIms(db.Model):
    __tablename__ = 'ops_ims_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), unique=True)
    cycle = db.Column(db.String(64))


# 安全作业计划明细
class OpsInfoSec(db.Model):
    __tablename__ = 'ops_sec_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), unique=True)
    cycle = db.Column(db.String(64))


# 智能网作业计划明细
class OpsInfoVpmn(db.Model):
    __tablename__ = 'ops_vpmn_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), unique=True)
    cycle = db.Column(db.String(64))


# 短号短信作业计划明细
class OpsInfoVss(db.Model):
    __tablename__ = 'ops_vss_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), unique=True)
    cycle = db.Column(db.String(64))


# 彩铃作业计划明细
class OpsInfoCl(db.Model):
    __tablename__ = 'ops_cl_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), unique=True)
    cycle = db.Column(db.String(64))
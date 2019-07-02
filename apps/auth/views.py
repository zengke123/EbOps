from . import auth
from .. import db
from ..models import User
from .forms import LoginForm
from datetime import datetime
from flask import render_template, request, url_for, flash, redirect, jsonify
from flask_login import login_user, login_required, logout_user, current_user


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 渲染HTML时需加入 {{ form.csrf_token }} 否则validate_on_submit一直为False
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        error = '用户或密码错误'
        if user is not None and user.verify_password(form.password.data):
            # 用户状态正常
            if user.status == 1:
                login_user(user, form.remember_me.data)
                # 记录登录时间
                login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user.last_time = login_time
                db.session.commit()
                # return redirect(url_for('main.index'))
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                error = "该用户已被锁定"
    return render_template("login.html", form=form, error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已退出登录")
    return redirect(url_for('main.index'))


@auth.route('/users')
@login_required
def users():
    # 返回用户列表
    all_users = User.query.all()
    return render_template("user_list.html", app='用户管理', action='用户列表', users=all_users)


@auth.route('/create', methods=['GET','POST'])
@login_required
def create():
    # 创建新用户
    if request.method == "GET":
        return render_template('user_create.html', app='用户管理', action='创建用户')
    else:
        user = request.form
        password1 = user.get('password1')
        password2 = user.get('password2')
        if password1 != password2:
            error = "两次密码不一致，请确认.."
            return render_template('user_create.html', app='用户管理', action='创建用户', error=error)
        else:
            role = 1 if user.get('role') == "Admin" else 0
            status = 1 if user.get('status') == "normal" else 0
            new_user = {
                'username': user.get('username'),
                'password': password1,
                'mail': user.get('email'),
                'role': role,
                'status': status,
                'create_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            _all_users = db.session.query(User.username).all()
            all_users = [x[0] for x in _all_users]
            if user.get('username') in all_users:
                error = "用户名已存在.."
                return render_template('user_create.html', app='用户管理', action='创建用户', error=error)
            else:
                add_user = User(**new_user)
                db.session.add(add_user)
                db.session.commit()
                return redirect(url_for('auth.users'))


@auth.route('/profile')
@login_required
def profile():
    # 返回个人信息
    user = User.query.filter(User.username == current_user.username).first()
    return render_template('user_profile.html', app='用户信息', user=user)


# 修改密码
@auth.route('/password', methods=['GET','POST'])
@login_required
def password():
    if request.method == "GET":
        return render_template('user_password.html', app='用户信息', action='密码更新')
    elif request.method == "POST":
        old_password = request.form.get('old_password')
        user = User.query.filter(User.username == current_user.username).first()
        if old_password == user.password:
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                error = "两次输入密码不一致"
        else:
            error = "原密码错误!"
        return render_template('user_password.html', app='用户信息', action='密码更新', error=error)


# 删除用户
# 根据id 删除设备信息
@auth.route('/delete', methods=["GET", "POST"])
@login_required
def delete():
    user_id = request.form.get('id')
    try:
        to_delete = User.query.filter(User.id == user_id).first()
        # 不能删除当前登录的管理员账户
        if to_delete.username == current_user.username:
            result = {"flag": "fail"}
        else:
            db.session.delete(to_delete)
            db.session.commit()
            result = {"flag": "success"}
    except Exception as e:
        print(str(e))
        result = {"flag": "fail"}
    return jsonify(result)


@auth.route('/get_uesr_info', methods=["GET", "POST"])
@login_required
def get_user_info():
    user_id = request.form.get('id')
    user_info = db.session.query(User).filter(User.id == user_id).one()
    result = {
        "flag": "success",
        "user_info": user_info.to_json()
    }
    print(result)
    return jsonify(result)


@auth.route('/modify_user_info', methods=["GET", "POST"])
@login_required
def modify_user_info():
    # 获取前端提交的json数据
    datas = request.get_json()
    try:
        user_id = datas.get('id')
        # 管理员状态不能更改为锁定
        to_update = User.query.filter(User.id == user_id).first()
        if to_update.username == current_user.username and datas.get('status') == '0':
            result = {"flag": "fail"}
        else:
            # update数据库表数据
            db.session.query(User).filter(User.id == user_id).update(datas)
            db.session.commit()
            result = {"flag": "success"}
    except Exception as e:
        print(str(e))
        result = {"flag": "fail"}
    # request中要求的数据格式为json，为其他会导致前端执行success不成功
    return jsonify(result)


def change_user_status(user_list, status):
    if user_list:
        for username in user_list:
            to_update = db.session.query(User).filter(User.username == username).one()
            to_update.status = status
        db.session.commit()
        return "success"
    else:
        return "fail"


# 激活用户
@auth.route('/active', methods=["GET", "POST"])
@login_required
def active():
    _users = request.form.get('users')
    _users_temp = _users.split(',')
    # 去除checkbox选择的无效选项，包括当前登录用户
    _users_list = [x for x in _users_temp if x != '' and x != 'on' and x != current_user.username]
    result = change_user_status(_users_list, '1')
    return result


# 禁用用户
@auth.route('/deactive', methods=["GET", "POST"])
@login_required
def deactive():
    _users = request.form.get('users')
    _users_temp = _users.split(',')
    _users_list = [x for x in _users_temp if x != '' and x != 'on' and x != current_user.username]
    result = change_user_status(_users_list, '0')
    return result


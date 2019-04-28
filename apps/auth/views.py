from . import auth
from .. import db
from ..models import User
from .forms import LoginForm
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user


@auth.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    # 渲染HTML时需加入 {{ form.csrf_token }} 否则validate_on_submit一直为False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已退出登录")
    return redirect(url_for('main.index'))


@auth.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template("user_list.html", app='用户管理', action='用户列表', users=users)


@auth.route('/create', methods=['GET','POST'])
@login_required
def create():
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
                'role': role,
                'status': status
            }
            add_user = User(**new_user)
            db.session.add(add_user)
            db.session.commit()
            return redirect(url_for('auth.users'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('user_profile.html', app='用户信息')
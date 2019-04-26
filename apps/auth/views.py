from . import auth
from ..models import User
from .forms import LoginForm
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user


@auth.route("/login",methods=['GET','POST'])
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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
import config


# 创建SQLAlchemy实例
db = SQLAlchemy()
# 创建celery配置
celery = Celery(__name__, broker='redis://localhost:6379/0')
# 创建用户管理
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 登录视图对应蓝图auth的login
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # 初始化数据库
    db.init_app(app)
    # 初始化用户管理
    login_manager.init_app(app)
    # 更新celery配置
    celery.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/1',
        worker_concurrency=1,
        worker_prefetch_multiplier=1,
        imports=('apps.ops.tasks',),
        result_expires=1800,
        timezone='Asia/Shanghai',
        enable_utc=True,
        task_send_sent_event=True
    )
    # 蓝本注册
    # 用户认证模块
    from .auth import auth as auth_blueprint
    # 主页
    from .main import main as main_blueprint
    # 作业计划模块
    from .ops import ops as ops_blueprint
    # 自动例检
    from .check import check as check_blueprint
    # 资产管理
    from .assets import assets as assets_blueprint
    # 统计数据
    from .tongji import tongji as tongji_blueprint
    # 统一对外接口蓝本
    from .api_1 import api_1 as api_1_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, url_prefix='')
    app.register_blueprint(ops_blueprint, url_prefix='/ops')
    app.register_blueprint(check_blueprint, url_prefix='/check')
    app.register_blueprint(assets_blueprint, url_prefix='/assets')
    app.register_blueprint(tongji_blueprint, url_prefix='/tongji')
    app.register_blueprint(api_1_blueprint, url_prefix='/api/v1')
    return app

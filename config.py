import os
from datetime import timedelta
# 调试模式
DEBUG = True
# SECRET_KEY设置当CSRF启用时有效，这将生成一个加密的token供表单验证使用
SECRET_KEY = os.urandom(24)
# 设置session的超时时间
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

# 数据库配置
# mysql版本5.5以下的 mysqlconnector的版本必须为2.1
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = 'zengke'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'webapp'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                                                       HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SCHEDULER_API_ENABLED = True
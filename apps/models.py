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


class Host(db.Model):
    """
    表名: host
    id: 业务平台
    platform: 平台
    cluster: 集群名称
    hostname: 主机名称
    device_type: 设备类型
    manufacturer: 设备厂家
    device_model: 设备型号
    serial: 序列号
    account: 账户
    version: 业务版本
    software_version: 软件模块版本号
    local_ip: 内网IP地址
    nat_ip: 映射IP地址
    os_version: 操作系统版本
    engine_room: 所在机房
    frame_number: 机架号
    power_frame_number: 电源柜
    net_time: 入网时间
    s_period: 软件过保时间
    h_period: 硬件过保时间
    status: 状态
    power: 功率
    """
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, autoincrement=True)
    platform = db.Column(db.String(32), nullable=False)
    cluster = db.Column(db.String(32), primary_key=True, nullable=False)
    hostname = db.Column(db.String(64), primary_key=True, nullable=False)
    device_type = db.Column(db.String(32), nullable=False)
    manufacturer = db.Column(db.String(32))
    device_model = db.Column(db.String(32))
    serial = db.Column(db.String(32))
    account = db.Column(db.String(32))
    version = db.Column(db.String(64))
    software_version = db.Column(db.String(64))
    local_ip = db.Column(db.String(64))
    nat_ip = db.Column(db.String(64))
    os_version = db.Column(db.String(64))
    engine_room = db.Column(db.String(64))
    frame_number = db.Column(db.String(32))
    power_frame_number = db.Column(db.String(32))
    net_time = db.Column(db.Date)
    s_period = db.Column(db.Date)
    h_period = db.Column(db.Date)
    power = db.Column(db.String(32))
    status = db.Column(db.String(32))

    def to_json(self):
        return {
                "id": self.id,
                "platform": self.platform,
                "cluster": self.cluster,
                "hostname": self.hostname,
                "device_type": self.device_type,
                "manufacturer": self.manufacturer,
                "device_model": self.device_model,
                "serial": self.serial,
                "account": self.account,
                "version": self.version,
                "software_version": self.software_version,
                "local_ip": self.local_ip,
                "nat_ip": self.nat_ip,
                "os_version": self.os_version,
                "engine_room": self.engine_room,
                "frame_number": self.frame_number,
                "power_frame_number": self.power_frame_number,
                "net_time": self.net_time,
                "period": self.period,
                "status": self.status
                }
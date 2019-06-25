from . import db
from flask_login import UserMixin
from . import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    mail = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default=0)
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

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "mail": self.mail,
            "role": self.role,
            "status": self.status,
            "create_time": self.create_time,
            "last_time": self.last_time
        }


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
    """
    id: 编号
    t_name: 类型(ops_items中的t_name)
    item_id: 作业计划单项编号
    content: 标题内容
    cycle: 执行周期
    item_detail: 执行明细
    createtime: 创建时间
    """
    __tablename__ = 'ops_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(64), index=True)
    item_id = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)
    cycle = db.Column(db.String(64))
    item_detail = db.Column(db.Text)
    createtime = db.Column(db.String(64))


# 作业计划明细
class OpsResult(db.Model):
    """
    id: 编号
    t_name: 类型(ops_items中的t_name)
    item_id: 作业计划单项编号,与ops_info一致
    date: 执行日期
    time: 执行时间
    s_times: 执行成功次数
    f_times: 执行失败次数
    result: 执行结果
    log_id: 任务编号,日志编号
    """
    __tablename__ = 'ops_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.String(64), index=True)
    date = db.Column(db.DATE, index=True)
    time = db.Column(db.Time, index=True)
    s_times = db.Column(db.SmallInteger, default=0)
    f_times = db.Column(db.SmallInteger, default=0)
    result = db.Column(db.String(255))
    log_id = db.Column(db.String(64), primary_key=True)

    def to_json(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "date": str(self.date),
            "time": str(self.time),
            "s_times": self.s_times,
            "f_times": self.f_times,
            "result": self.result,
            "log_id": self.log_id
        }


# 作业计划完整执行情况
class OpsEvent(db.Model):
    """
    id: 编号
    log_id: 任务编号，与ops_result中log_id一致
    cluster: 检查的网元
    hostname: 主机名称
    status: 任务执行状态，成功、失败
    result: 执行结果
    reason: 失败原因（默认为空）
    """
    __tablename__ = 'ops_event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(64), index=True)
    cluster = db.Column(db.String(64))
    hostname = db.Column(db.String(64), index=True)
    status = db.Column(db.String(64))
    result = db.Column(db.Text, nullable=True)
    reason = db.Column(db.Text, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "log_id": self.log_id,
            "item_id": self.item_id,
            "cluster": self.cluster,
            "hostname": self.hostname,
            "status": self.status,
            "result": self.result,
            "reason": self.reason
        }


# 自动例检相关表模型
# 例检主机
class CheckHost(db.Model):
    """
    id: 编号
    node: 业务平台节点
    cluster: 集群名称
    hostname: 主机名
    """
    __tablename__ = 'c_host'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node = db.Column(db.String(32), index=True, nullable=False)
    cluster = db.Column(db.String(32), index=True, nullable=False)
    hostname = db.Column(db.String(32), unique=True, nullable=False)


# 例检历史记录
class CheckHistory(db.Model):
    """
    id: 编号
    checktime: 例检时间
    hostname: 主机名称
    type: 类型(主机,集群)
    operator: 操作员
    """
    __tablename__ = 'c_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checktime = db.Column(db.String(64), index=True, nullable=False)
    hostname = db.Column(db.String(32), index=True, nullable=False)
    type = db.Column(db.String(32), nullable=False)
    operator = db.Column(db.String(32), nullable=False)


# 资产管理相关表模型
# 主机信息
class Host(db.Model):
    """
    表名: host
    id: id
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
    net_time = db.Column(db.Date, default='2000-01-01')
    s_period = db.Column(db.Date, default='2000-01-01')
    h_period = db.Column(db.Date, default='2000-01-01')
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
                "s_period": self.s_period,
                "h_period": self.h_period,
                "power": self.power,
                "status": self.status
                }

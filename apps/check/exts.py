import os
import time
import datetime
import requests
from .. import db
from .. import celery
from ..models import CheckHistory
from celery.utils.log import get_task_logger
from ..settings import CHECK_DOWNLOAD_FOLDER, TASKS_LOG_FOLDER

logger = get_task_logger(__name__)


def auto_check(lj_type, name):
    import pexpect
    username = "root"
    password = '123456'
    cmd = 'zj zjlj lj:type={},name={}'.format(lj_type, name)
    flag = None
    result = None
    try:
        child = pexpect.spawn('telnet 0 47303', timeout=600)
        child.expect('login:')
        child.sendline(username)
        child.expect('password:')
        child.sendline(password)
        child.expect('root > ')
        child.sendline(cmd)
        child.expect('{}root >')
        result_temp = child.before
        # result_temp = b'zj zjlj lj:type=jq,name=SICP01\r\nRETN=0006, DESC=\r\n'
        result = result_temp.decode(encoding="utf-8")
        result = result.split('\r\n')[1]
        if 'RETN=0000' in result:
            flag = "success"
        else:
            flag = "fail"
        child.sendline('quit')
        child.close()
    except Exception:
        flag = "fail"
    finally:
        return flag, result


@celery.task
def req_zjlj(api_name, name, operator):
    logger.info('[%s] 执行自动例检 [%s] "%s"', operator, name, api_name)
    # 接口url
    url = "http://192.168.27.51:8188/CHECK/ZJLJ"
    if api_name and api_name != 'null':
        payload = api_name
        r = requests.post(url, json=payload, timeout=1800)
        try:
            result = r.json()
            if result.get('code') == "00000000":
                report_name = down_report(api_name, operator)
                return {'description':'success', 'report':report_name}
            else:
                return result
        except Exception as e:
            logger.info(str(e))
            return "http请求失败 " + str(r.status_code)
    else:
        return "参数错误"

@celery.task(bind=True)
def test_check(self, lj_type, name, operator):
    cmd = 'zj zjlj lj:type={},name={}'.format(lj_type, name)
    print(cmd)
    # id = celery.Task.request
    print(self.request.id)
    log_name = TASKS_LOG_FOLDER + str(self.request.id) + '.log'
    for i in range(10):
        with open(log_name, 'a') as f:
            f.write('[{}]测试状态'.format(self.request.id) + str(i) + '\n')
            time.sleep(5)
    return "success", "RETURN=0000"


def down_report(api_name, operator):
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # omscc4.0自动例检日志存放目录
    src_path = "/home/opsweb/zjlj/output/*"
    # web备份目录 DOWNLOAD_FOLDER，用于下载例检报告
    dst_path = CHECK_DOWNLOAD_FOLDER + str(name)
    os.mkdir(dst_path)
    cp_cmd = "cp -R {} {}".format(src_path, dst_path)
    os.system(cp_cmd)
    os.environ['name'] = str(name)
    tmd_cmd = "tar zcf ${name}.tar.gz * --remove-files;rm -rf host"
    os.chdir(dst_path)
    os.system(tmd_cmd)
    host_type = api_name.get('type')
    hostname = api_name.get('name')
    new_type = "集群" if host_type == "jq" else "主机"
    add_log = CheckHistory(checktime=name, hostname=hostname, type=new_type, operator=operator)
    db.session.add(add_log)
    db.session.commit()
    return str(name)


@celery.task
def req_pllj(api_name, name, operator):
    logger.info('[%s] 执行批量例检 [%s] "%s"', operator, name, api_name)
    # 接口url
    url = "http://192.168.27.51:8188/CHECK/ZJLJ"
    if api_name and api_name != 'null':
        payload = api_name
        r = requests.post(url, json=payload, timeout=1800)
        try:
            result = r.json()
            if result.get('code') == "00000000":
                # 替换原始主机名称
                api_name['name'] = name
                report_name = down_report(api_name, operator)
                return {'description':'success', 'report':report_name}
            else:
                return result
        except Exception as e:
            logger.info(str(e))
            return "http请求失败 " + str(r.status_code)
    else:
        return "参数错误"


def schedule_check(items):
    import time, datetime
    from collections import namedtuple
    CheckItem = namedtuple("CheckItem", "type name")
    temp_items = items.split("|")
    check_items = []
    for item in temp_items:
        type_name = item.split("_")[0]
        hostname = item.split("_")[1]
        check_items.append(CheckItem(type=type_name, name=hostname))

    for item in check_items:
        print(datetime.datetime.now(), "例检 {} {}".format(item.type, item.name))
        api_name = {'type': item.type, 'name': item.name}
        zjlj_task = req_zjlj.delay(api_name, item.name, "Scheduler")
        time.sleep(1)
    return "success"


def test_schedule_check(items):
    import time, datetime
    from collections import namedtuple
    CheckItem = namedtuple("CheckItem","type name")
    temp_items = items.split("|")
    check_items =[]
    for item in temp_items:
        type_name = item.split("_")[0]
        hostname = item.split("_")[1]
        check_items.append(CheckItem(type=type_name, name=hostname))

    for item in check_items:
        print(datetime.datetime.now(), "例检 {} {}".format(item.type,item.name))
        time.sleep(5)
        print(datetime.datetime.now(), "例检完成")
        time.sleep(5)
    return "success"


def add_job_scheduler(handler, job_id, job_cron, args):
    minute, hour, day, month, day_of_week = job_cron.split(",")
    if day_of_week != "*":
        day_of_week = int(day_of_week) - 1
    _job_args = {
        'func': schedule_check,
        'id': str(job_id),
        'args': args,
        'misfire_grace_time':300,
        'trigger': {
            'type': 'cron',
            'day_of_week': day_of_week,
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute
        }
    }
    # misfire_grace_time:因为某种特定的原因导致定时任务服务挂掉，在重启后如果任务的时间和实际的时间的差值小于定义的misfire_grace_time
    print(_job_args)
    handler.add_job(**_job_args)
from .. import celery
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def zyjh(api_name, name, operator):
    import time
    logger.info('[%s] 执行作业计划 [%s] "%s"', operator, name, api_name)
    time.sleep(20)
    return {'RETN': '00000000', 'DESC': 'OK'}


# 调用api执行作业计划
# name, operator参数用于页面展示
@celery.task
def req_zyjh(api_name, name, operator):
    logger.info('[%s] 执行作业计划 [%s] "%s"', operator, name, api_name)
    # 接口url
    url = "http://192.168.27.51:8188/CCZYJH/ZNWZY"
    if api_name and api_name != 'null':
        payload = {'TYPE': api_name}
        try:
            r = requests.post(url, json=payload, timeout=1800)
            result = r.json()
            return result
        except Exception as e:
            logger.info(str(e))
            return "fail"
    else:
        return "fail"
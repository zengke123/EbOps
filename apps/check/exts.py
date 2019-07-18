import os
import time
import datetime
from ..settings import CHECK_DOWNLOAD_FOLDER


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


def test_check(lj_type, name):
    cmd = 'zj zjlj lj:type={},name={}'.format(lj_type, name)
    print(cmd)
    time.sleep(4)
    return "success", "RETURN=0000"


def down_report():
    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # omscc4.0自动例检日志存放目录
    src_path = "/home/omscc/zengke/output/*"
    # web备份目录 DOWNLOAD_FOLDER，用于下载例检报告
    dst_path = CHECK_DOWNLOAD_FOLDER + str(name)
    os.mkdir(dst_path)
    cp_cmd = "cp -R {} {}".format(src_path, dst_path)
    os.system(cp_cmd)
    os.environ['name'] = str(name)
    tmd_cmd = "tar zcf ${name}.tar.gz * --remove-files;rm -rf host"
    os.chdir(dst_path)
    os.system(tmd_cmd)
    return str(name)
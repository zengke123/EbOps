import datetime
from flask import render_template


# 日期处理
def get_date_range(delta_day):
    today = datetime.datetime.now().strftime("%Y%m%d")
    # 转为datetime格式，用于日期计算，str格式无法计算
    begin_date = datetime.datetime.strptime(today, "%Y%m%d") - datetime.timedelta(delta_day)
    dates = []
    dt = begin_date
    date = begin_date.strftime("%Y%m%d")
    while date <= today:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

# 数据整理
def t_rows(titles, data):
    result = []
    if isinstance(data, list):
        for item_data in data:
            rows = [item_data.get(k, "") for k in titles]
            result.append(rows)
    # 兼容返回格式为dict, 而不是list
    elif isinstance(data, dict) and data:
        rows = [data.get(k, "") for k in titles]
        result.append(rows)
    else:
        result = [['无记录'] + ["" for _ in range(len(titles) -1)]]
    return result

def handle_vpmn(phonenumber, data, *args):
    v_user_list = data.get('VuserList', '')
    as_user_list = data.get('AsuserList', '')
    home_user_list = data.get('HomeuserList', '')
    sicp_user_list = data.get('SicpuserList', '')
    result = {
        "vpmn_flag":  1 if  v_user_list else 0,
        "as_flag": 1 if as_user_list else 0,
        "home_flag": 1 if home_user_list else 0,
        "sicp_flag": 1 if sicp_user_list or (v_user_list and home_user_list) else 0,
        "sicp_check": 1 if v_user_list and home_user_list and not sicp_user_list else 0
    }

    return render_template('complaint_vpmn.html', app='投诉处理', action="智能网业务", phonenumber=phonenumber,
                           v_user_list=v_user_list, as_user_list=as_user_list,
                           home_user_list=home_user_list, sicp_user_list=sicp_user_list, result=result)



def handle_crbt(phonenumber, data, *args):
    crbt_user_list = data.get('UserList', '')
    del_user_list = data.get('DeleteUserList', '')
    copy_log_list = data.get('CopyLogList', '')
    wl_club_list = data.get('WireLessClubList', '')
    user_depot_list = data.get('UserDepotList', '')
    user_ring_list = data.get('UserRingList', '')
    grp_ring_list = data.get('UserGrpRingList', '')
    set_ring_list = data.get('CrbtSeRingList', '')
    result = {
        "crbt_flag": crbt_user_list[0].get("grpflag") if isinstance(crbt_user_list, list) else "",
        "as_flag": crbt_user_list[0].get("isvolte") if isinstance(crbt_user_list, list) else "",
        "userring_flag": 1 if user_ring_list else 0
    }
    # 铃音设置类型
    set_ring_map = {
        '0': '播放basicRingIndex指定的铃音',
        '1': '循环播放个人铃音库的铃音',
        '4': '单首包月音乐盒',
        '5': '包月音乐盒轮播',
        '6': '播放个人铃音轮'
    }

    if crbt_user_list:
        set_ring_type = str(crbt_user_list[0].get("ringtype"))
        crbt_user_list[0]["ringtype"] = set_ring_type + ": " + set_ring_map.get(set_ring_type)

    return render_template('complaint_crbt.html', app='投诉处理', action="彩铃业务", **locals())


def handle_vrbt(phonenumber, data, *args):
    vrbt_user_list = data.get('VrbtUserList', '')
    del_user_list = data.get('VrbtDeUserList', '')
    vrbt_ring_list = data.get('VrbtRingList', '')
    mrbt_ring_list = data.get('MrbtRingList', '')
    set_ring_list = data.get('VrbtSeRingList', '')
    result = {
        "vrbt_flag": vrbt_user_list[0].get("vflag") if isinstance(vrbt_user_list, list) else ""
    }
    return render_template('complaint_vrbt.html', app='投诉处理', action="视频彩铃业务", **locals())


def handle_ctx(phonenumber, data, *args):
    CtxuserList = data.get('CtxuserList', '')
    user_data = []
    if isinstance(CtxuserList, list):
        data = CtxuserList[0]
        titles = ["vpnnumber", "phonenumber", "grp_name", "grpid", "createtime", "useroutlock", "userinlock",
                  "clipflag", "tshortflag", "cfuflag", "cfbflag", "cfnryflag", "cfnrcflag", "limit",
                  "callbarflag1", "callbarflag2", "callbarflag3", "callbarflag4"]
        title_map = {
            "vpnnumber": {'info': '用户短号码'},
            "phonenumber": {'info': '用户号码'},
            "grp_name": {'info': '集团名称'},
            "grpid": {'info': '集团ID'},
            "createtime": {'info': '用户开户时间'},
            "useroutlock": {
                'info': '用户呼出闭锁标识',
                'value': {
                    '0': '未封锁',
                    '1': '封锁'
                }
            },
            "userinlock": {
                'info': '用户呼入闭锁标识',
                'value': {
                    '0': '未封锁',
                    '1': '封锁'
                }
            },
            "clipflag": {
                'info': '主叫号码显示业务标识',
                'value': {
                    '0': '未开通',
                    '1': '开通'
                }
            },
            "tshortflag": {
                'info': '被叫短号显示标志',
                'value': {
                    '0': '长号显示',
                    '1': '短号显示'
                }
            },
            "cfuflag": {
                'info': '无条件前转业务标识',
                'value': {
                    '0': '未开通',
                    '1': '开通，未设置号码',
                    '2': '开通，已设置号码'
                }
            },
            "cfbflag": {
                'info': '遇忙前转业务标识',
                'value': {
                    '0': '未开通',
                    '1': '开通，未设置号码',
                    '2': '开通，已设置号码'
                }
            },
            "cfnryflag": {
                'info': '无应答前转业务标识',
                'value': {
                    '0': '未开通',
                    '1': '开通，未设置号码',
                    '2': '开通，已设置号码'
                }
            },
            "cfnrcflag": {
                'info': '未注册前转业务标识',
                'value': {
                    '0': '未开通',
                    '1': '开通，未设置号码',
                    '2': '开通，已设置号码'
                }
            },
            "limit": {'info': '并发呼出限制个数'},
            "callbarflag1": {
                'info': '紧急呼叫权限',
                'value': {
                    '0': '无权限',
                    '1': '有权限'
                }
            },
            "callbarflag2": {
                'info': '长途呼出权限',
                'value': {
                    '0': '无权限',
                    '1': '有权限'
                }
            },
            "callbarflag3": {
                'info': '国际呼出权限',
                'value': {
                    '0': '无权限',
                    '1': '有权限'
                }
            },
            "callbarflag4": {
                'info': '本地呼出权限',
                'value': {
                    '0': '无权限',
                    '1': '有权限'
                }
            }
        }
        for item in titles:
            name = title_map[item]['info'] + " ({})".format(item)
            value = data.get(item)
            # 数据字典
            value_dict = title_map.get(item).get('value', "")
            # 字段说明
            value_info = ": " + value_dict.get(str(value)) if isinstance(value_dict, dict) else ""
            row = [name, str(value) + value_info]
            user_data.append(row)
    return render_template('complaint_ctx.html', app='投诉处理', action="Centrex业务",
                           phonenumber=phonenumber, ctx_user_list=CtxuserList, user_data=user_data)


def handle_vpmn_rec(phonenumber, data, *args):
    req_date = args[0]
    cs_titles = ['RecHost', 'ServiceKey', 'CallType', 'ChargeType', 'RoamFlag', 'CallingPartyNumber',
                 'CalledPartyNumber', 'RoamAreaNumber', 'MSInfoVLRNumber', 'MSInfoLAI', 'MSInfoCellId',
                 'CallBeginTime', 'CallEndTime', 'CallDuration', 'AccountFlag', 'RecType']
    lte_titles = ['RecHost', 'ServiceKey', 'CallType', 'ChargeType', 'RoamFlag', 'CallingPartyNumber',
                  'CalledPartyNumber', 'CallBeginTime', 'CallEndTime', 'CallDuration', 'AccountFlag', 'ECGI', 'TACID',
                  'RecType']
    # 整理数据
    rec_list = data.get('VpmnUserRecList', '')
    lterec_list = data.get('VpmnUserLteRecList', '')
    cs_rows = t_rows(cs_titles, rec_list)
    lte_rows = t_rows(lte_titles, lterec_list)
    return render_template('complaint_v_rec.html', app='投诉处理', action="V网话单", **locals())


def handle_vpmn_home(phonenumber, data, *args):
    req_date = args[0]
    cs_titles = ['RecHost', 'ServiceKey', 'CallType', 'CallingPartyNumber', 'CalledPartyNumber', 'MSInfoVLRNumber',
                   'MSInfoLAI',
                   'MSInfoCellId', 'CallBeginTime', 'CallEndTime', 'CallDuration', 'RecType']
    lte_titles = ['RecHost', 'ServiceKey', 'CallType', 'CallingPartyNumber', 'CalledPartyNumber', 'CallBeginTime',
                  'CallEndTime', 'CallDuration', 'ECGI', 'TACID', 'RecType']
    # 整理数据
    rec_list = data.get('HomeUserRecList', '')
    lterec_list = data.get('HomeUserLteRecList', '')
    cs_rows = t_rows(cs_titles, rec_list)
    lte_rows = t_rows(lte_titles, lterec_list)
    return render_template('complaint_v_rec.html', app='投诉处理', action="合家欢话单", **locals())


def handle_vpmn_frd(phonenumber, data, *args):
    req_date = args[0]
    cs_titles = ['RecHost', 'ServiceKey', 'CallType', 'CallingPartyNumber', 'CalledPartyNumber', 'MSInfoVLRNumber',
                   'MSInfoLAI',
                   'MSInfoCellId', 'CallBeginTime', 'CallEndTime', 'CallDuration', 'RecType']
    lte_titles = ['RecHost', 'ServiceKey', 'CallType', 'CallingPartyNumber', 'CalledPartyNumber', 'CallBeginTime',
                  'CallEndTime', 'CallDuration', 'ECGI', 'TACID', 'RecType']
    # 整理数据
    rec_list = data.get('FrdUserRecList', '')
    lterec_list = data.get('FrdUserLteRecList', '')
    cs_rows = t_rows(cs_titles, rec_list)
    lte_rows = t_rows(lte_titles, lterec_list)
    return render_template('complaint_v_rec.html', app='投诉处理', action="朋友圈话单", **locals())
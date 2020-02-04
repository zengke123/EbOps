import json
import requests
from . import complaint
from ..settings import API_URL
from .exts import handle_vpmn, handle_crbt, handle_vrbt, handle_ctx
from flask import render_template, request, jsonify
from flask_login import login_required


# 接口api映射
# 参数：对应接口API，视图渲染函数
apis = {
    "vpmn": ("SCPUSERDATA", handle_vpmn),
    "ctx": ("CTXUSERDATA", handle_ctx),
    "crbt": ("CRBTUSERDATA", handle_crbt),
    "vrbt": ("VRBTUSERDATA", handle_vrbt),
    "portlog": ("USERPORTLOG", ""),
    "vpmn_rec": ("VPMNUSERRECORD", ""),
    "frd_rec": ("FRDUSERRECORD", ""),
    "home_rec": ("HOMEUSERRECORD", "")
}


# 调用api
def req_ccautomate(api_type, phonenumber, date=None):
    item_type = apis.get(api_type)[0]
    if item_type:
        api_url = API_URL + item_type
        if not date:
            payload = {'phone': phonenumber}
        else:
            payload = {'phone': phonenumber, 'date': date}
        try:
            r = requests.post(api_url, json=payload)
            result = r.json()
            return result
        except json.decoder.JSONDecodeError:
            print("return result error: not json")
            return False
    else:
        print("request fail")
        return False


@complaint.route('/', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        print(">>> REQ:", request.form)
        api_name = request.form.get("api")
        phonenumber = request.form.get("phonenumber")
        req_date = request.form.get("date")
        result = req_ccautomate(api_name, phonenumber, date=req_date)
        print("<<< ACK", result)
        handle_func = apis.get(api_name)[1]
        if callable(handle_func):
            return handle_func(phonenumber, result)
        else:
            return jsonify(result)
    else:
        return render_template('complaint.html', app='投诉处理')




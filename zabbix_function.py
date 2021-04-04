import requests
import json
import csv
import sys


# Zabbix POST 요청 함수
# method: API Method / params: Json Data / auth: 인증 정보
def post_api_request(method, params, auth):
    url = "http://192.168.137.15/zabbix/api_jsonrpc.php"
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": auth,
        "id": 0
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

# Zabbix Login 정보 입력 및 리턴 함수
def get_credentials():
    # user = input("ID: ")
    # pw = getpass.getpass("PW: ")
    user = "Admin"
    pw = "zabbix"
    return user, pw

# Zabbix Login 후 auth 토큰 리턴 함수
def login(user, pw):
    params = {"user": user, "password": pw}
    result = post_api_request("user.login", params, None)
    auth = result["result"]
    return auth

# 입력: auth, host / 출력: hostid
def get_hostid(*args):
    params = {
        "output": "extend",
        "filter": {
            "name": [args[1]]
        }
    }
    result = post_api_request("host.get", params, args[0])
    try:
        return result["result"][0]["hostid"]
    except:
        return None

# 입력: auth / 출력: result
def get_hostid_all(*args):

    params = {
        "output": "extend",
        "selectTriggers": "extend"
    }

    result = post_api_request("host.get", params, args[0])
    try:
        return result["result"]
    except:
        return None

# 입력: auth, triggerid / 출력: result
def update_trigger(*args):

    params = {
        "triggerid": args[1],
        "status": 0
    }

    result = post_api_request("trigger.update", params, args[0])
    try:
        return result["result"]
    except:
        return None

def create_host(auth, host, ip, groupids, templateids):
    if get_hostid(auth, host) is not None:
        print("Host: %s exist" % host)
    else:
        params = {
            "host": host,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [{"groupid": groupid} for groupid in groupids],
            "templates": [{"templateid": templateid} for templateid in templateids],
        }

        result = post_api_request("host.create", params, auth)
        print("Host: %s is added" % host)
        return host


# 입력: group 이름 / 출력: groupid
def get_groupid(*args):
    params = {
        "output": "extend",
        "filter": {
            "name": [args[1]]
        }
    }
    result = post_api_request("hostgroup.get", params, args[0])
    return result["result"][0]["groupid"]


# 입력: template 이름 / 출력: templateid
def get_templateid(*args):
    params = {
        "output": "extend",
        "filter": {
            "name": [args[1]]
        }
    }
    result = post_api_request("template.get", params, args[0])
    return result["result"][0]["templateid"]


if __name__ == "__main__":

    user, pw = get_credentials()
    auth = login(user, pw)

    host_results = get_hostid_all(auth)
    for host_result in host_results:

        print("============================\n")
        print(host_result["name"])
        count = 0

        for host_trigger in host_result["triggers"]:
            #print(host_trigger)
            count += 1

            ## status(1 = Disabled, 2 = Enabled)
            ## value(1 = Problem, 2 = OK)
            if host_trigger["status"] == "1":

                print(count, host_trigger["triggerid"], host_trigger["description"], host_trigger["status"], host_trigger["value"])
                print(update_trigger(auth, host_trigger["triggerid"]))












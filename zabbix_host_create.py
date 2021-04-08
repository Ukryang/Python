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
    #user = input("ID: ")
    #pw = getpass.getpass("PW: ")
    user = "Admin"
    pw = "zabbix"
    return user, pw

# Zabbix Login 후 auth 토큰 리턴 함수
def login(user, pw):
    params = {"user": user, "password": pw }
    result = post_api_request("user.login", params, None)
    auth = result["result"]
    return auth

# 입력: auth, host / 출력: hostid
def get_hostid(*args):

    params = {
        "output": "extend",
        "filter": {
            "name": [ args[1] ]
        }
    }
    result = post_api_request("host.get", params, args[0])
    try:
        return result["result"][0]["hostid"]
    except:
        return None

# 입력: auth, host / 출력: hostid
def get_hostid_all(*args):

    params = {
        "output": "extend"
    }

    result = post_api_request("host.get", params, args[0])
    try:
        return result["result"][0]["hostid"]
    except:
        return None

def create_host(auth, host, ip, groupids, templateids):
    if get_hostid(auth, host) is not None:
        print("Host: %s exist" %host)
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
            "groups": [{ "groupid": groupid } for groupid in groupids],
            "templates": [{ "templateid": templateid } for templateid in templateids],
        }

        result = post_api_request("host.create", params, auth)
        print("Host: %s is added" %host)
        return host

# 입력: group 이름 / 출력: groupid
def get_groupid(*args):

    params = {
        "output": "extend",
        "filter": {
            "name": [ args[1] ]
        }
    }
    result = post_api_request("hostgroup.get", params, args[0])
    return result["result"][0]["groupid"]

# 입력: template 이름 / 출력: templateid
def get_templateid(*args):

    params = {
        "output": "extend",
        "filter": {
            "name": [ args[1] ]
        }
    }
    result = post_api_request("template.get", params, args[0])
    return result["result"][0]["templateid"]

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("csv is required")
        sys.exit(1)
    filename = sys.argv[1]

    user, pw = get_credentials()
    auth = login(user, pw)

    # 파일 데이터를 불러와 읽어 드림
    with open("zabbix_list/"+filename, newline="", encoding="utf-8-sig") as f:
        # csv 파일 인식 후 읽어 드림
        reader = csv.reader(f)

        # 라인 별로 분리하여 추출(구분자 ",")
        for r in reader:
            host = r[0]
            ip = r[1]
            hostgroups = r[2]
            templates = r[3]

            # 다중 호스트 그룹 분리 후 배열 저장
            hostgroups = hostgroups.split(",")

            # 다중 템플릿 분리 후 배열 저장
            templates = templates.split(",")

            # 빈 배열 생성
            groupids = []
            templateids = []

            i = 0

            # 호스트 그룹아이디 추출 후 배열 저장
            while i < len(hostgroups):
                groupids.append(get_groupid(auth, hostgroups[i]))
                i += 1

            # i 초기화
            i = 0

            # 템플릿 아이디 추출 후 배열 저장
            while i < len(templates):
                templateids.append(get_templateid(auth, templates[i]))
                i += 1

            create_host(auth, host, ip, groupids, templateids)





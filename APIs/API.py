import json, requests, http.client

# 계정 정보
with open('APIS/account.json') as account:
    account = json.load(account)
    id, pw = account["id"], account["pw"]


# 디미고인 로그인 및 토큰 반환
def dimigoIn_Login():
    req = requests.post("https://api.dimigo.in/auth", json={"id": id, "password": pw}, headers={'Content-Type': 'application/json; charset=utf-8'})

    if req.status_code == 200:
        return json.loads(req.text)["token"], json.loads(req.text)["refresh_token"]

    return req.status_code

# 디미고인 토큰 갱신
def dimigoIn_Refresh(refresh_token: str):
    req = requests.post("https://api.dimigo.in/auth/token/refresh", headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {refresh_token}'})

    if req.status_code == 200:
        return json.loads(req.text)["token"], json.loads(req.text)["refresh_token"]

    return req.status_code

# 디미고인 인강실 신청 목록
def dimigoIn_IngangList(access_token: str):
    req = requests.post("http://api.dimigo.in/ingang/users/myklass", headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {access_token}'})

    if req.status_code == 200:
        return json.loads(req.text)["users"]

    return req.status_code


# 디미고라이프 로그인 및 토큰 반환
def dimigoLife_Login():
    req = requests.post("https://api.dimigo.life/auth/authorize", json={"username": id, "password": pw}, headers={'Content-Type': 'application/json; charset=utf-8'})

    if req.status_code == 200:
        return req.headers.get("Set-Cookie").split("=")[1].split(";")[0]

    return req.status_code

# 디미고인 빨래 신청자 명단
def dimigoLife_LaundryList(access_token):
    conn = http.client.HTTPSConnection("api.dimigo.life")
    conn.request("GET", "/washer/table?ss=ss", '', {'Cookie': f'Life_Auth={access_token}; Path=/; HttpOnly'})
    res = conn.getresponse()
    data = res.read()

    machine_list = [machine for machine in json.loads(data.decode("utf-8")).get("data")]
    array = list()
    temp = list()
    result = list()

    for machine in machine_list:
        for applier in machine.get("applies"):
            if applier.get("user") is not None:
                array.append({
                    "hour": int(applier.get("time")[11:13])+9,
                    "minute": int(applier.get("time")[14:16]),
                    "name": str(applier.get("user")).split("'")[5],
                    "serial": str(applier.get("user")).split("'")[8].split(" ")[1].split("}")[0]
                })
            else:
                array.append({
                    "hour": int(applier.get("time")[11:13]) + 9,
                    "minute": int(applier.get("time")[14:16])
                })

    for element in enumerate(array):
        prev = array[element[0]-1].get('hour')
        now = element[1].get('hour')
        passCon = True if not element[0] else False if element[0] == len(array)-1 else prev < now

        if passCon:
            temp.append(element[1])
        else:
            result.append(temp)
            temp = list()

    return result

dimigoLife_LaundryList(dimigoLife_Login())
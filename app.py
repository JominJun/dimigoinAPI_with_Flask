from flask import Flask, render_template
from APIs import API as api
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    dimigoIn_access_token, dimigoIn_refresh_token = api.dimigoIn_Login()
    dimigoLife_access_token = api.dimigoLife_Login()

    ingangList = [person for person in api.dimigoIn_IngangList(dimigoIn_access_token)]
    laundryList = api.dimigoLife_LaundryList(dimigoLife_access_token)
    processedLaundryList = list()

    for washer in laundryList:
        for person in washer:
            if person.get("serial") is not None and '15' in person.get("serial")[0:2]:
                reserved_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                                  datetime.datetime.now().day, person.get("hour"), person.get("minute"))
                left_time = (
                            reserved_time - datetime.datetime.now()).seconds if reserved_time > datetime.datetime.now() else 0
                processedLaundryList.append(
                    {"hour": person.get("hour"), "minute": person.get("minute"), "left_time": left_time,
                     "name": person.get("name")})

    temp = list()
    temptemp = list()
    processedIngangList = list()

    for person in ingangList:
        temp.append(person.get("name"))

    for person in enumerate(ingangList):
        if temp.count(person[1].get("name")) == 1:
            processedIngangList.append({"name": person[1].get("name"), "time": [person[1].get("time")]})
        else:
            if not person[1].get("name") in temptemp:
                temptemp.append(person[1].get("name"))
                processedIngangList.append({"name": person[1].get("name"), "time": [1, 2]})

    hour, minute = int(datetime.datetime.now().strftime('%H')), int(datetime.datetime.now().strftime('%M'))
    integrated_time = int(str(hour)+str(minute))
    now_time = 0
    
    if 19 <= hour <= 22:
        if 1950 <= integrated_time <= 2110:
            now_time = 1
        elif 2110 < integrated_time <= 2250:
            now_time = 2
            
    #now_time = 2 #테스트용

    return render_template("index.html", ingangList=processedIngangList, laundryList=processedLaundryList, now_time=now_time)


if __name__ == '__main__':
    app.run()

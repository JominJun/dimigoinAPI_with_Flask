from flask import Flask, render_template
from APIs import API as api
import time, datetime

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
                reserved_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, int(person.get("time").split("시")[0]))
                left_time = (reserved_time - datetime.datetime.now()).seconds if reserved_time > datetime.datetime.now() else 0
                processedLaundryList.append({"time": person.get("time"), "left_time": left_time, "name": person.get("name")})

    return render_template("index.html", ingangList=ingangList, laundryList=processedLaundryList)


if __name__ == '__main__':
    app.run()
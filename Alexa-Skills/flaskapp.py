from pymongo import MongoClient


import logging, requests, json, thread

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

con = MongoClient('mongodb://smelly:smell@ds119370.mlab.com:19370/smell_security')
db = con.smell_security



app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ownerCursor = db.UserFav.find_one({"person":"owner"})
ownerID = ownerCursor["smellID"]

friendCursor = db.UserFav.find_one({"person":"friend"})
friendID = friendCursor["smellID"]

smellmap = {}
smellmap[0] = "OFF"
smellmap[1] = "GREEN"
smellmap[2] = "AQUA"
smellmap[3] = "MAGENTA"
smellmap[4] = "WHITE"
smellmap[5] = "EMERALD"
smellmap[6] = "FREE_GREEN"
smellmap[7] = "SPRING"
smellmap[8] = "DODGER"
smellmap[9] = "BLUE2"
smellmap[10] = "BLUE"
smellmap[11] = "PURPLE"
smellmap[12] = "ELECTRIC"
smellmap[13] = "SUN"
smellmap[14] = "ICE"


def febreze(title,x):
    #   print "888888888888888888888888888888888888888888888888888888888888888"
    print type(title)
    url = "https://na-hackathon-api.arrayent.io:443/v3/devices/50331668"




    headers = {
        'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiI3OGQ1MmY0MC0wMTUzLTExZTctYWU0Ni01ZmMyNDA0MmE4NTMiLCJlbnZpcm9ubWVudF9pZCI6Ijk0OGUyY2YwLWZkNTItMTFlNi1hZTQ2LTVmYzI0MDQyYTg1MyIsInVzZXJfaWQiOiI5MDAwMTA0Iiwic2NvcGVzIjoie30iLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwiaWF0IjoxNDg4Njg0NjI2LCJleHAiOjE0ODk4OTQyMjZ9.dcBtnmO2Pa9Na8hRuxvsjTWEnNVBm630cZhtf1OLYEVE1r7s24IWoL4zyQqZpwpmTz_gX8zqZUYk9Yzv6cIizA",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "28e38285-01ad-15eb-d74f-03ed7d4336ae"
    }
    title = int(title)
    print type(title)
    if (title == 1):
        ownerSmell = db.UserFav.find_one({"person":"owner"})
        print 'owneronweronwerownerowenrowenr'
        print ownerSmell["smellID"]

        payload = "[{\"DeviceAction\": \"alarm_enable=0\" },{\"DeviceAction\": \"led_mode=1\" }, {\"DeviceAction\": \"led_color=0,"+str(ownerSmell["smellID"])+",2,4,4\" },{\"DeviceAction\": \"home_state=1\"}]"

    elif (title ==2):
        print 99999999999999999999999
        friendSmell = db.UserFav.find_one({"person": "friend"})
        payload = "[{\"DeviceAction\": \"alarm_enable=0\" },{\"DeviceAction\": \"led_mode=2\" }, {\"DeviceAction\": \"led_color=0,4,"+str(friendSmell["smellID"])+",4,4\" },{\"DeviceAction\": \"home_state=1\"}]"

    elif (title==3):

        payload = "[{\"DeviceAction\": \"alarm_enable=1\"}]"
    else:
        payload = "[{\"DeviceAction\": \"alarm_enable=0\" },{\"DeviceAction\": \"led_mode=1\" }, {\"DeviceAction\": \"led_color=0,3,2,4,4\" },{\"DeviceAction\": \"home_state=1\"}]"

    try:
        response2 = requests.request("PUT", url, data=payload, headers=headers)
    except Exception as e:
        print(e)


def updateColor():
    global ownerCursor
    global ownerID
    ownerCursor = db.UserFav.find_one({"person": "owner"})
    ownerID = ownerCursor["smellID"]

    global friendCursor
    global friendID
    friendCursor = db.UserFav.find_one({"person": "friend"})
    friendID = friendCursor["smellID"]


@ask.launch
def new_session():
    global friendID
    global ownerID
    thread.start_new_thread(updateColor, ())
    response = requests.post("https://4e4dd181.ngrok.io/api/getpersoninfo/")
    message = " {}".format(json.loads(response.text)['Detail'])


    #message = "Changing Scents"
    title = " {}".format(json.loads(response.text)['Key'])
    #title = 1
    print "7777777777777777777777777777777777777777777777777777777777777"
    print title
    print 'Message is ', message
    thread.start_new_thread(febreze, (title, 1))
    # title = int(title)
    # if (title == 1):
    #     message = message + "Frebeze has switched on your favourite smell"
    # elif (title == 2):
    #     message = message + "Frebeze has switched on the favourite smell"

    return statement(message)

    #return statement(message)
    

@ask.intent("YesIntent")
def response():
    # response = requests.post("https://knockknockwho.herokuapp.com/api/getpersoninfo/")
    # message = "hello I am alexa"

    response = requests.post("https://4e4dd181.ngrok.io/api/getpersoninfo/")
    # return statement(message)
    message = " {}".format(json.loads(response.text)['Detail'])
    title = " {}".format(json.loads(response.text)['Key'])
    print "7777777777777777777777777777777777777777777777777777777777777"
    print title
    print 'Message is ', message
    thread.start_new_thread(febreze, (title, 1))

    return statement(message)

    #message = "hello I am alexa"
    #return statement(message)
    #message = render_template('random')
    #response = requests.post("http://10.0.0.207:8000/api/getpersoninfo/")
    #message = " {}".format(json.loads(response.text)['Detail'])
    #return statement("I am working")

    #message = render_template('alexaAnswer',answer = json.loads(response.text)['Detail'])
    #print response
    #return statement(message)
    #return statement(message)


@ask.session_ended
def session_ended():
    return "", 200



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8082)


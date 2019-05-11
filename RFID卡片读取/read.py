import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522
import requests
import time
import datetime
from flask import Flask, request
import thread

SLEEP_SECOND = 2
OPENED = False
REMOTE_SERVER_URL = "http://192.168.137.1:8000/data"

app = Flask(__name__)

def getValue(name, value):
    global OPENED
    while OPENED:
        reader = rc522()
        try:
            print("begin reading.")
            idid, info = reader.read()
            print("id is {}".format(idid))
            print("information is {}".format(info))
        except Exception as error:
           print("error is {}".format(error))
        finally:
            GPIO.cleanup()
        if idid != None:
            send_data = {"idid":"{}".format(idid), "info":"{}".format(info) }
            req = requests.post(REMOTE_SERVER_URL + "?data=" + str(send_data))
            print("time: " + str(datetime.datetime.now()))
            print("send {0}".format(send_data))
        time.sleep(SLEEP_SECOND)

@app.route('/', methods=['GET'])
def index():
    global OPENED
    if 'op' in request.args:
        if request.args['op'] == "on" and not OPENED:
            OPENED = True
            thread.start_new_thread(getValue, ("getValue", None))

        elif request.args['op'] == "off" and OPENED:
            OPENED = False
    return 'ok'

app.run(host='0.0.0.0')
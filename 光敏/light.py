import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522 as rc522
import requests
import time
import datetime
from flask import Flask, request
import thread

GPIO_LIGHT = 2
GPIO_LED = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LIGHT, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

SLEEP_SECOND = 2
OPENED = False
REMOTE_SERVER_URL = "http://192.168.137.1:8000/data"
l = ""

app = Flask(__name__)

def getValue(name, value):
    global OPENED
    while OPENED:
        global l
        l = GPIO.input(GPIO_LIGHT)
        if l > 0:
            GPIO.output(GPIO_LED, GPIO.HIGH)
            l = "Dark"
        else:
            GPIO.output(GPIO_LED, GPIO.LOW)
            l = "Light"
        if l != None:
            send_data = {"l":l}
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
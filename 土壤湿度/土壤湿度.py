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

GPIO.setmode(GPIO.BOARD)
soil_Pin = 3
GPIO.setup(soil_Pin, GPIO.IN)
LED_Pin = 7
GPIO.setup(LED_Pin, GPIO.OUT)
h = ""

def callback(channel1):
    if GPIO.input(channel1):
        global h 
        h = "dry"
        GPIO.output(LED_Pin, GPIO.LOW)
    else:
        global h
        h = "moisture"
        GPIO.output(LED_Pin, GPIO.HIGH)

# add simply event
GPIO.add_event_detect(soil_Pin, GPIO.BOTH, bouncetime = 200)
# add a time - triggered callback function
GPIO.add_event_callback(soil_Pin, callback)

app = Flask(__name__)

def getValue(name, value):
    global OPENED
    while OPENED:
        time.sleep(0.1)
        if h != None:
            send_data = {"h":h}
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
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts

from django.conf import settings

from my_iot.models import HistoryValue

def getValue():
    h = ''
    if settings.CURRENT_HUMIDITY == None:
        h = "无读数"
    else:
        h = str(settings.CURRENT_HUMIDITY)
    return h

def index(request):
    h = getValue()
    return render(request, 'my_iot/index.html', {'h':h})

@csrf_exempt
def communicate(request):
    if 'method' in request.GET:
        method = request.GET['method']
        data = request.GET['data']
        rts.get("http://127.0.0.1:3000/com" + "?data=" + data)
        return HttpResponse("ok")
    elif 'method' in request.POST:
        method = request.POST['method']
        data = request.POST['data']
        rts.post("http://127.0.0.1:3000/com", data={'data':data})
        return HttpResponse("ok")
    elif 'data' in request.GET:
        data = request.GET['data']
        print("I'm django received get data: " + data)
        return HttpResponse("ok")
    elif 'data' in request.POST:
        data = request.POST['data']
        print("I'm django received post data: " + data)
        return HttpResponse("ok")
    return render(request, 'my_iot/communicate.html')

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}".format(d['h']))
        value = HistoryValue(humidity=d['h'])
        value.save()
        settings.CURRENT_HUMIDITY = d['h']
    if 'get' in request.GET:
        rts.get("http://192.168.137.195:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        h = getValue()
        return HttpResponse(json.dumps({'h': h}))
    return HttpResponse("ok")
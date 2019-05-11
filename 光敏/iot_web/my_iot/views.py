from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts

from django.conf import settings

from my_iot.models import HistoryValue

def getValue():
    l = ''
    if settings.CURRENT_LIGHT == None:
        l = "无读数"
    else:
        l = str(settings.CURRENT_LIGHT)
    return l

def index(request):
    l = getValue()
    return render(request, 'my_iot/index.html', {'l':l})

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
        print("get data {0}".format(d['l']))
        value = HistoryValue(light=d['l'])
        value.save()
        settings.CURRENT_LIGHT = d['l']
    if 'get' in request.GET:
        rts.get("http://192.168.137.195:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        l = getValue()
        return HttpResponse(json.dumps({'l': l}))
    return HttpResponse("ok")
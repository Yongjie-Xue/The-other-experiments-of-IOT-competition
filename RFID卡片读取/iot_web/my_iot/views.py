from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts

from django.conf import settings

from my_iot.models import HistoryValue

def getValue():
    idid = ''
    info = ''
    if settings.CURRENT_IDID == None:
        idid = "无读数"
    else:
        idid = str(settings.CURRENT_IDID)
    if settings.CURRENT_INFO == None:
        info = "无读数"
    else:
        info = str(settings.CURRENT_INFO)
    return idid, info

def index(request):
    idid, info = getValue()
    return render(request, 'my_iot/index.html', {'idid':idid, 'info':info})

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
        print("get data {0}, {1}".format(d['idid'], d['info']))
        value = HistoryValue(idid=d['idid'], info=d['info'])
        value.save()
        settings.CURRENT_IDID = d['idid']
        settings.CURRENT_INFO = d['info']
    if 'get' in request.GET:
        rts.get("http://192.168.137.195:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        idid, info = getValue()
        return HttpResponse(json.dumps({'idid':idid, 'info': info}))
    return HttpResponse("ok")
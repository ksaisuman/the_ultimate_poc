from django.shortcuts import render
from django.http import HttpResponse
import json
# from metrics import REQUEST_COUNT


def hello(request):
    res = {'result': []}
    with open('dummy.txt', 'r') as f:
        for line in f:
            res['result'].append(json.loads(line))
    # REQUEST_COUNT.labels('get', '/hello', 200).inc()
    return HttpResponse(json.dumps(res))

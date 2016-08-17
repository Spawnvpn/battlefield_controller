import json
import socket
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def index(request):
    quantity = request.POST.get('quantity')
    if quantity:
        session['quantity'] = quantity
        return redirect('/form/')
    return render(request, 'index.html')


def form(request):
    try:
        session['armies_units']
    except KeyError:
        session['armies_units'] = list()
        session['armies_squads'] = list()
        session['armies_strategy'] = list()

    if request.method == 'POST':
        session['armies_units'].append(request.POST.get('units'))
        session['armies_squads'].append(request.POST.get('squads'))
        session['armies_strategy'].append(request.POST.get('strategy'))
        if len(session['armies_units']) == int(
                session['quantity']):
            battle_data = dict(
                quan_armies=int(session['quantity']),
                units=session['armies_units'], squads=session['armies_squads'],
                strategy=session['armies_strategy'])
            dump = json.dumps(battle_data)
            sock.connect(('', 9090))
            dump = str.encode(dump)
            sock.send(dump)
            return HttpResponse('/result')
    return render(request, 'form.html')


def result(request):
    return render(request, 'result.html')


@csrf_exempt
def data_render(request):
    data = sock.recv(4096)
    data = bytes.decode(data)
    return JsonResponse(data, safe=False)


session = SessionStore()
sock = socket.socket()

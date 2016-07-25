from battlefield import battle
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore


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
            go = battle.Battlefield(
                quan_armies=int(session['quantity']),
                units=session['armies_units'], squads=session['armies_squads'],
                strategy=session['armies_strategy'])
            go.start()
            session['winner'] = go.winner
            session['log'] = go.battle_log
            return HttpResponse('/result')
    return render(request, 'form.html')


def result(request):
    winner = session['winner']
    log = session['log']
    return render(request, 'result.html', context={'winner': winner,
                                                   'log': log})


session = SessionStore()

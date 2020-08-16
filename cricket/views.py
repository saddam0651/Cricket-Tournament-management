from django.shortcuts import render
from .models import *
# Create your views here.


def index(request):
    points = Point.objects.all().order_by('-points')
    context = {'points': points}
    return render(request, 'index.html', context)


def matches(request):
    matches = Match.objects.filter(result__isnull=True)
    context = {'matches': matches}
    return render(request, 'match.html', context)


def results(request):
    matches = Match.objects.filter(result__isnull=False)
    context = {'matches': matches}
    return render(request, 'result.html', context)


def teams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'team.html', context)


def players(request, id):
    players = Player.objects.filter(team=id)
    context = {'players': players}
    return render(request, 'player.html', context)


def points(request):
    points = Point.objects.all().order_by('-points')
    context = {'points': points}
    return render(request, 'point.html', context)

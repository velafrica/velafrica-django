from django.conf import settings
from django.shortcuts import render_to_response
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.core import serializers

from velafrica.stock.models import Category, Product
from velafrica.counter.models import Entry

def home(request):
  return render_to_response('base.html')

def counter(request):
  entries = Entry.objects.all()
  today = entries.first()
  velos_total = 0
  for entry in entries:
    velos_total += entry.amount
  print("velos " + str(velos_total))
  velos_total_str = str(velos_total)
  return render_to_response('counter/index.html', { 'velos_total': velos_total_str, 'velos_today': today.amount })

"""
def listPlayers(request):
  p = sorted(Player.objects.all(), key=lambda a: a.get_pointsInt(), reverse=True)
  return render_to_response('base_players.html', {'page_content':p}, context_instance=RequestContext(request))

def playersJSON(request):
  data = serializers.serialize('json', Player.objects.all())
  response = HttpResponse(str(data))
  response['Access-Control-Allow-Origin'] = '*'
  response['Content-Type'] = 'application/json; charset=utf-8'
  response['Access-Control-Allow-Headers'] = '*'
  response['Vary'] = 'Accept-Encoding'
  response['Cache-Control'] = 'No-Cache'
  return response

def playersJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Player.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response

def listPlayersDetail(request, playerID):
  p = Player.objects.get(id=playerID)
  return render_to_response('base_players_detail.html',{'player':p}, context_instance=RequestContext(request))

def playersDetailJSON(request, playerID):
  data = serializers.serialize('json', Player.objects.filter(id=playerID))
  response = HttpResponse(str(data))
  response['Access-Control-Allow-Origin'] = '*'
  response['Content-Type'] = 'application/json; charset=utf-8'
  response['Access-Control-Allow-Headers'] = '*'
  response['Vary'] = 'Accept-Encoding'
  response['Cache-Control'] = 'No-Cache'
  return response



def listGames(request):
  g = Game.objects.all().order_by('date')
  return render_to_response('base_games.html', {'page_content':g},context_instance=RequestContext(request))

def gamesJSON(request):
  data = serializers.serialize('json', Game.objects.all())
  response = HttpResponse(str(data))
  response['Access-Control-Allow-Origin'] = '*'
  response['Content-Type'] = 'application/json; charset=utf-8'
  response['Access-Control-Allow-Headers'] = '*'
  response['Vary'] = 'Accept-Encoding'
  response['Cache-Control'] = 'No-Cache'
  return response


def gamesJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Game.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response


def listGamesDetail(request, gameID):
  g = Game.objects.get(id=gameID)
  p = Point.objects.filter(game=gameID)
  return render_to_response('base_games_detail.html',{'game':g,'points':p}, context_instance=RequestContext(request))

@login_required(login_url='/auth/login/')
def profile(request):
  return render_to_response('user/profile.html', {'request':request}, context_instance=RequestContext(request))

def logout_view(request):
  logout(request)
  return redirect('/auth/login/')

def seasonsJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Season.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response


def seasonsJSON(request):
  data = serializers.serialize('json', Season.objects.all())
  response = HttpResponse(str(data))
  response['Access-Control-Allow-Origin'] = '*'
  response['Content-Type'] = 'application/json; charset=utf-8'
  response['Access-Control-Allow-Headers'] = '*'
  response['Vary'] = 'Accept-Encoding'
  response['Cache-Control'] = 'No-Cache'
  return response

def pointsJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Point.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response

def pointtypesJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', PointType.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response
  
def teamsJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Team.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response
  
def leaguesJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', League.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response 

def listLeagues(request):
  l = League.objects.all()
  return render_to_response('base_leagues.html', {'page_content':l},context_instance=RequestContext(request))
  
def cardsJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Card.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response  
  
def locationsJSONP(request):
  callback = request.GET.get('callback','f')
  data = callback + "("+str(serializers.serialize('json', Location.objects.all()))+")"
  response =  HttpResponse(data)
  response['Content-Type'] = 'application/javascript; charset=utf-8'
  return response  
  """
import pdb

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.conf import settings
import json
from lib.database import DB

#~ from django.contrib.auth import authenticate, login
import django.contrib.auth as dAuth


def index(request):
	
	if not request.user.is_authenticated():
		#~ return render(request, 'wallstreet/login.html')
		return HttpResponse('User not authenticated')
	
	return render(request, 'wallstreet/plot.html')
    
    
def get_eod(request, symbol, start_date=None, end_date=None):

	if not request.user.is_authenticated():
		msg = { error: 'Not authenticated' }
		return HttpResponse(json.dumps(msg), content_type="application/json")
		
	db = DB(settings.YAHOO_DATABASE)
	rows = db.get_eod(symbol, start_date, end_date)
	return HttpResponse(json.dumps(rows), content_type="application/json")


def login(request):

	if request.method == 'GET':
		
		return render(request, 'wallstreet/login.html')
		
	elif request.method == 'POST':
		
		username = request.POST.get('inputName', None)
		password = request.POST.get('inputPassword', None)
		
		user = dAuth.authenticate(username=username, password=password)
	
		if user is not None:
		
			if user.is_active: 
				
				dAuth.login(request, user)
				return render(request, 'wallstreet/plot.html')
				
			else:
				return HttpResponse('User not active')
		
		else:
			return HttpResponse('Invalid login')


def logout(request):
	
	dAuth.logout(request)
	return render(request, 'wallstreet/login.html')

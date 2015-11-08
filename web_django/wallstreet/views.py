from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.conf import settings
import json
from lib.database import DB


def index(request):
    return render(request, 'wallstreet/index.html')
    
    
def get_eod(request, symbol, start_date=None, end_date=None):

	db = DB(settings.YAHOO_DATABASE)
	rows = db.get_eod(symbol, start_date, end_date)
	return HttpResponse(json.dumps(rows), content_type="application/json")

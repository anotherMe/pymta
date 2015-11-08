
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    # get_eod (symbol, start_date)
    url(r'^get_eod/(?P<symbol>\D+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})', 
		views.get_eod, name='get_eod'),
    url(r'^get_eod/(?P<symbol>\D+)/(?P<start_date>\d{4}-\d{2}-\d{2})', views.get_eod, name='get_eod'),
    url(r'^get_eod/(?P<symbol>\D+)', views.get_eod, name='get_eod'),
    
    ### \d{4}-\d{2}-\d{2} --> 2015-31-01
]

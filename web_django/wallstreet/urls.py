
from django.conf.urls import url
from . import views

urlpatterns = [

	# /

    url(r'^$', views.index, name='index'),
    
    
    # /login
    
    url(r'^login', views.login, name='login'),
    

    # /logout
    
    url(r'^logout', views.logout, name='logout'),
    
    
    # /get_eod/
    
    url(r'^get_eod/(?P<symbol>\D+)/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})', 
		views.get_eod, name='get_eod'),
    url(r'^get_eod/(?P<symbol>\D+)/(?P<start_date>\d{4}-\d{2}-\d{2})', views.get_eod, name='get_eod'),
    url(r'^get_eod/(?P<symbol>\D+)', views.get_eod, name='get_eod'),
    
]

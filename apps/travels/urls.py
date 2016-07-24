from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^logout$', views.logout),
	url(r'^travels$', views.travel_dashboard),
	url(r'^travels/process_trip_request$', views.process_trip),
	url(r'^travels/add$', views.add_trip),
	url(r'^travels/destination/(?P<id>\d+)$', views.destination), # accepts two paths: travels/destination/###
	url(r'^travels/destination/(?P<id>\d+)/$', views.destination), # OR: travels/destination/###/
	url(r'^join/(?P<id>\d+)$', views.join_trip)
]
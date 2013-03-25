'''
Created on Mar 24, 2013

@author: fan wei fang
'''
from django.conf.urls.defaults import *
from models import Note
from django.views.generic import ListView, DetailView
notes = Note.objects.all()

urlpatterns = patterns(
    '',
    (r'^$',
     ListView.as_view(queryset=notes)),
    (r'^note/(?P<slug>[-\w]+)/$',
     DetailView.as_view(queryset=notes, slug_field='slug')),
    (r'^create/$','notes.views.create_note'),
    (r'^note/(?P<slug>[-\w]+)/update/$','notes.views.update_note'),
)
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('Matches/', matches, name='matches'),
    path('Results/', results, name='results'),
    path('Teams/', teams, name='teams'),
    path('Players/<int:id>/', players, name='players'),
    path('Points/', points, name='points'),
]
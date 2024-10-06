from django.urls import path
from .views import *

urlpatterns = [
    path('index',Index, name='index'),
    path('create-or-join-room',create_or_join_room , name='create_or_join_room'),    
    path('create-room',create_room , name='create_room'),    
    path('join-room',join_room , name='join_room'),    
    path('tic-tac-toe/<str:room_code>/',tic_tac_toe_room, name='tic_tak_toe_room')
]

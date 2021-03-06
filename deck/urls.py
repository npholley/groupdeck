from django.conf.urls import include, url
import views

urlpatterns = [
   url(r'^$', views.Landing.as_view(), name="deck-home"),
   url(r'^room/(?P<slug>.+)/(?P<key>.+)/', views.Room.as_view(), name="game-room-key"), 
   url(r'^room/(?P<slug>.+)/', views.Room.as_view(), name="game-room-slug"), 
   url(r'^room/', views.Room.as_view(), name="game-room"),
   url(r'^create/room/', views.RoomCreate.as_view(), name="create-room"),  
   url(r'^create/deck/', views.DeckManage.as_view(), name="create-deck"),  
   url(r'^create/card/', views.CardCreate.as_view(), name="create-card"),  
   url(r'^update/room/(?P<slug>.+)/', views.RoomUpdate.as_view(), name="update-room"),
   url(r'^update/deck/(?P<slug>.+)/', views.DeckManage.as_view(), name="update-deck"),
   url(r'^update/card/(?P<pk>.+)/', views.CardUpdate.as_view(), name="update-card"), 
   url(r'^delete/room/(?P<slug>.+)/', views.RoomDelete.as_view(), name="delete-room"), 
   url(r'^delete/deck/(?P<slug>.+)/', views.DeckDelete.as_view(), name="delete-deck"), 
   url(r'^delete/card/(?P<pk>.+)/', views.CardDelete.as_view(), name="delete-card"),  
]
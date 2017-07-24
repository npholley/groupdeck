from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import models, serializers 
from datetime import datetime
from braces.views import CsrfExemptMixin
from django.db.models import Q
from json import loads
import permissions as deckpermissions

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSimpleSerializer
    queryset = models.CustomUser.objects.all()
    lookup_field = ('username')
    permission_classes = (permissions.IsAuthenticated,
        deckpermissions.IsUserOrAdmin)

class CardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CardSerializer
    queryset = models.Card.objects.filter(in_deck=False)
    lookup_field = ('pk')
    permission_classes = (permissions.IsAuthenticated,
        deckpermissions.ReadOnlyOrCreate)
    
    def get_queryset(self):
        since = self.request.query_params.get('since', None)
        search = self.request.query_params.get('search', None)
        queryset = models.Card.objects.filter(in_deck=False)

        if since is not None:
            last_time = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
            queryset = queryset.filter(date_edited__gte=last_time)
        if search is not None:
            queryset = queryset.filter(text__icontains = search)
            
        return queryset

class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeckSimpleSerializer
    queryset = models.Deck.objects.all()
    lookup_field = ('slug')
    permission_classes = (permissions.IsAuthenticated,
        deckpermissions.IsOwnerOrReadOnly)
    
    def get_queryset(self):
        since = self.request.query_params.get('since', None)
        queryset = models.Deck.objects.filter(user_created = self.request.user)
        search = self.request.query_params.get('search', None)
        in_play = self.request.query_params.get('in_play', None)
        
        if since is not None:
            last_time = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
            queryset = queryset.filter(date_edited__gte=last_time)
        if search is not None:
            queryset = queryset.filter(name__icontains = search)
        if in_play is not None:
            queryset = queryset.filter(in_play = search)
            
        return queryset

    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        deck = get_object_or_404(queryset, slug=slug)
        serializer = serializers.DeckSerializer(deck)
        return Response(serializer.data)

class GameRoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GameRoomSimpleSerializer
    queryset = models.GameRoom.objects.all()
    lookup_field = ('slug')
    permission_classes = (deckpermissions.IsPlayer,
        deckpermissions.IsOwnerOrReadOnly)

    def get_queryset(self):
        since = self.request.query_params.get('since', None)
        queryset = models.GameRoom.objects.all()
        
        if since is not None:
            last_time = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
            queryset = queryset.filter(date_edited__gte=last_time)
            
        return queryset

    @detail_route()
    def get_current_card(self, request, slug=None):
        try:
            obj = self.get_object()
            self.check_object_permissions(request, obj)
            serializer = serializers.CardSimpleSerializer(obj.deck.card_displayed, many=False)
            return Response(serializer.data,
                status=status.HTTP_200_OK)
        except Exception, e:
            print e
            return Response({'status': 'Error grabbing card'},
                status=status.HTTP_400_BAD_REQUEST)

    @detail_route(permission_classes=[deckpermissions.CanDraw, deckpermissions.IsPlayer])
    def draw_card(self, request, slug=None):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        drawn_card = obj.deck.draw_card()
        if drawn_card:
            serializer = serializers.CardSimpleSerializer(drawn_card, many=False)
            return Response(serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Deck is empty'},
                status=status.HTTP_200_OK)

    @detail_route(permission_classes=[deckpermissions.IsOwner])
    def start_game(self, request, slug=None):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        serializer = serializers.DeckSerializer(obj.play_deck(), many=False)
        return Response(serializer.data,
            status=status.HTTP_200_OK)

    @detail_route(permission_classes=[deckpermissions.IsOwner])
    def stop_game(self, request, slug=None):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        serializer = serializers.GameRoomSerializer(obj.stop_play(), many=False)
        return Response(serializer.data,
            status=status.HTTP_200_OK)

    @detail_route(permission_classes=[deckpermissions.IsOwner])
    def close_room(self, request, slug=None):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        obj.close_room()
        return Response({'status': 'Room closed'},
            status=status.HTTP_200_OK)

    @detail_route(permission_classes=[deckpermissions.IsOwner])
    def reset_deck(self, request, slug=None):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        serializer = serializers.GameRoomSerializer(obj.reset_deck(), many=False)
        return Response(serializer.data,
            status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(request, obj)
        serializer = serializers.GameRoomSerializer(obj)
        return Response(serializer.data)
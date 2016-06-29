# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import markdown
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status, filters, permissions
from velafrica.organisation.models import *
from velafrica.organisation.serializer import *
from velafrica.sbbtracking.models import *
from velafrica.sbbtracking.serializer import *
from velafrica.stock.models import *
from velafrica.stock.serializer import *

class DjangoModelPermissionsMixin(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions,)


@api_view(('GET',))
def api_root(request, format=None):
    """
    This is the API of Velafrica (www.velafrica.ch)

    If you build something cool with it and want to show it to us, please do not hesitate!

    Send a link with description to nikolai.raeber (at) velafrica.ch

    Have fun!
    """

    queryset = Tracking.objects.none()

    from velafrica.api import urls
    from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

    URL_NAMES = []
    def load_url_pattern_names(namespace, patterns):
        """Retrieve a list of urlpattern names"""
        URL_NAMES = []
        
        for pat in patterns:
            if pat.__class__.__name__ == 'RegexURLResolver':            # load patterns from this RegexURLResolver
                URL_NAMES.append(load_url_pattern_names(pat.namespace, pat.url_patterns))
            elif pat.__class__.__name__ == 'RegexURLPattern':           # load name from this RegexURLPattern
                # fully qualified pattern name :) (namespace::name)
                
                if pat.name is not None and pat.name not in URL_NAMES:
                    URL_NAMES.append((pat.name, pat.callback.__doc__))
        return (namespace, URL_NAMES)

    #root_urlconf = __import__(settings.ROOT_URLCONF)        # access the root urls.py file
    url_tree = load_url_pattern_names(None, urls.urlpatterns)   # access the "urlpatterns" from the ROOT_URLCONF

    response = {}
    for namespace_set in url_tree[1]:
        namespace = namespace_set[0]
        urls = namespace_set[1]
        namespace_urls = {}
        for ur in urls:
            if namespace:
                fqpn = '{}:{}'.format(namespace, ur[0])
                rev = ""
                try:
                    rev = reverse(str(fqpn), request=request, format=format)
                except:
                    try:
                        rev = reverse(str(fqpn), request=request, format=format, kwargs={'pk':1})
                    except:
                        print "something went wrong.. who cares :)"
                        pass
                    pass

                description = "{}".format(ur[1])
                namespace_urls[rev] = description.strip()
        response[namespace] = namespace_urls

    return Response(response)

class VeloTypeList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all velo types.
    """
    queryset = VeloType.objects.all()
    serializer_class = VeloTypeSerializer


class VeloTypeDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = VeloType.objects.all()
    serializer_class = VeloTypeSerializer

class TrackingList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all trackings.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer


class TrackingDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = Tracking.objects.all()
    serializer_class = TrackingDetailSerializer


class TrackingEventList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all tracking events.
    """

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer


class TrackingEventDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer


class TrackingEventTypeList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all trackings.
    """

    queryset = TrackingEventType.objects.all()
    serializer_class = TrackingEventTypeSerializer


class TrackingEventTypeDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of a trackings.
    """

    queryset = TrackingEventType.objects.all()
    serializer_class = TrackingEventTypeSerializer


class OrganisationList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all organisations.
    """

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class OrganisationDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of an organisation.
    """

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class WarehouseList(DjangoModelPermissionsMixin, generics.ListCreateAPIView):
    """
    Get a list of all warehouses.
    """

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetail(DjangoModelPermissionsMixin, generics.RetrieveUpdateAPIView):
    """
    Get details of an warehouse.
    """

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

'''

class LeagueList(generics.ListCreateAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


# League detail
class LeagueDetail(generics.RetrieveUpdateAPIView):

    queryset = League.objects.all()
    serializer_class = LeagueDetailSerializer


class ClubList(generics.ListCreateAPIView):

    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class ClubDetail(generics.RetrieveUpdateAPIView):

    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class PlayerList(generics.ListCreateAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['last_name', 'first_name']
    ordering = ['last_name', 'first_name']


class PlayerDetail(generics.RetrieveUpdateAPIView):
    """
    Get details about a special player.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class CompetitionList(generics.ListCreateAPIView):
    """
    Get a list of all the competitions.
    """
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class GameList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = Game.objects.all()
    serializer_class = GameDetailSerializer


class GameParticipationList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class GameParticipationDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = GameParticipation.objects.all()
    serializer_class = GameParticipationSerializer


class TeamList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class TeamDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = Team.objects.all()
    serializer_class = TeamInsightSerializer


class GameSchedule(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    serializer_class = GameSerializer

    def get_queryset(self):

        queryset = Team.objects.all()

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_games()


class RefereeList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = Referee.objects.all()
    serializer_class = RefereeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class RefereeDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = Referee.objects.all()
    serializer_class = VenueSerializer


class VenueList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class VenueDetail(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class SeasonList(generics.ListCreateAPIView):
    """
    Todo: document.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']


class NextGameByTeamId(generics.RetrieveUpdateAPIView):
    """
    Todo: document.
    """
    queryset = Team.objects.all()
    serializer_class = GameSerializer

    def get_object(self):

        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_next_game()


class LastGameByTeamId(generics.RetrieveUpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = GameSerializer

    def get_object(self):

        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj.get_last_game()


@api_view(['GET'])
def get_team_games_by_season(request, pk, season):
    """

    :param request:
    :param pk:
    :param season:
    :return:
    """
    team = Team.objects.get(id=pk)
    games = team.get_games_by_season(season)
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUser(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        u_email = serializer.data['username']
        if u_email is not None:
            VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.fields]
            serialized = UserSerializer(data=self.request.DATA)
            if serialized.is_valid():
                user_data = {field: data for (field, data) in self.request.DATA.items() if field in VALID_USER_FIELDS}
                user_data.update(email=u_email)
                user = get_user_model().objects.create_user(
                    **user_data
                )
                text = 'Thanks for registering on swissrugbystats.ch! You can now log in and add your favorite teams.'
                send_mail('Thanks for registering', text, 'christian.glatthard@rugbygear.ch', [u_email], fail_silently=False)
                return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFavorite(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FavoriteSerializer
        elif self.request.method == "GET":
            return FavoriteDetailSerializer

    def perform_create(self, serializer):
        u = self.request.user
        tid = serializer.data['team']
        t = Team.objects.get(id=tid)
        #f = Favorite(team=t, user=u)
        favs = Favorite.objects.filter(team=t, user=u)
        if len(favs) > 0:
            raise ResourceAlreadyExists()
        f = Favorite(team=t, user=u)
        f.save()
'''
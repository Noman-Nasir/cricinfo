from django.db.models import F
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cricinfo.authentications import IsSuperUserOrReadOnly, IsVerifiedUser
from teams.models import PlayerVisitCounter, Player, Team
from teams.serializers import PlayerSerializer, TeamSerializer


class PlayerViewSet(ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all().order_by('first_name', 'last_name')
    permission_classes = [IsSuperUserOrReadOnly, ]

    def retrieve(self, request, *args, **kwargs):
        player = self.get_object()
        player_visit_count, _ = PlayerVisitCounter.objects.get_or_create(player_id=player.id)
        player_visit_count.visit_count = F('visit_count') + 1
        player_visit_count.save()
        super(PlayerViewSet, self).retrieve(request, *args, **kwargs)
        serializer = self.get_serializer(player)
        return Response(serializer.data)


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all().order_by('name')
    permission_classes = (IsSuperUserOrReadOnly,)


@api_view(['GET'])
@permission_classes(permission_classes=(IsVerifiedUser,))
def get_most_visited_player(request):
    # Using Raw Sql in this view as practice
    most_visited_player = PlayerVisitCounter.objects.raw(
        '''SELECT teams_playervisitcounter.id,
        teams_playervisitcounter.player_id,
        teams_playervisitcounter.visit_count,
        MAX(teams_playervisitcounter.visit_count)
        AS visit_count__max
        FROM teams_playervisitcounter
        GROUP BY teams_playervisitcounter.id
        ORDER BY visit_count__max DESC
        LIMIT 1'''
    )[0].player

    serializer = PlayerSerializer(most_visited_player, context={'request': request})

    return Response({'player': serializer.data, 'visit_count': most_visited_player.playervisitcounter.visit_count})


@api_view(['GET'])
@permission_classes(permission_classes=(IsVerifiedUser,))
def get_player_stats_based_on_type(request):
    valid_player_roles = [Player.BATTER, Player.BOWLER, Player.WICKETKEEPER, Player.ALLROUNDER]
    if 'player_role' in request.query_params and request.query_params["player_role"] in valid_player_roles:
        player_role = request.query_params["player_role"]
        player_visits = PlayerVisitCounter.objects.filter(player__role=player_role).order_by('-visit_count')

        if not player_visits:
            return Response({'messgae': 'No player with this Role Visited'})

        most_visited_player = player_visits[0].player
        serializer = PlayerSerializer(most_visited_player, context={'request': request})
        return Response({'player': serializer.data, 'visit_count': player_visits[0].visit_count})

    else:
        return Response({
            'error': 'Query Parameter must specify Player Role',
            'valid player roles': valid_player_roles
        })

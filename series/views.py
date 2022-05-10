from datetime import date

from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cricinfo.authentications import IsVerifiedUser
from .models import Ground, Match, Series
from .serializers import SeriesSerializer, GroundSerializer, MatchSerializer


class SeriesViewSet(ModelViewSet):
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()


class MatchViewSet(ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    @action(methods=['put'], detail=True)
    def remove_series(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except Match.DoesNotExist:
            raise NotFound(f'Match with {pk=} does not exist.')

        match.series = None
        match.save()

        return Response({'success': 'Match is removed From the series.'}, status=200)

    @action(methods=['get'], detail=False)
    def recent(self, request):

        recent_matches = Match.objects.filter(match_date__lt=date.today())
        serializer = MatchSerializer(data=recent_matches, many=True)
        serializer.is_valid()

        return Response(
            {'success': True,
             'data': serializer.data,
             'error': False
             }
            , status=200
        )

    @action(methods=['get'], detail=False)
    def upcoming(self, request):

        upcoming_matches = Match.objects.filter(match_date__gt=date.today())
        serializer = MatchSerializer(data=upcoming_matches, many=True)
        serializer.is_valid()

        return Response(
            {'success': True,
             'data': serializer.data,
             'error': False
             }
            , status=200
        )

    @action(methods=['get'], detail=False)
    def live(self, request):

        live_matches = Match.objects.filter(match_date=date.today())
        serializer = MatchSerializer(data=live_matches, many=True)
        serializer.is_valid()

        return Response(
            {'success': True,
             'data': serializer.data,
             'error': False
             }
            , status=200
        )

    @action(methods=['post'], detail=True, url_path=r'set_series/(?P<series_id>\d+)')
    def set_series(self, request, pk=None, series_id=None):
        error_response = dict()

        try:
            series = Series.objects.get(id=series_id)
        except Series.DoesNotExist:
            raise NotFound(f'Series with {series_id=} does not exist.')

        try:
            match = Match.objects.get(id=pk)
        except Match.DoesNotExist:
            raise NotFound(f'Match with {pk=} does not exist.')

        if match.match_date < series.start_date:
            error_response['invalid_date'] = f'Match date can not be before series start date.'
            return Response(error_response, status=400)
        if match.match_date > series.end_date:
            error_response['invalid_date'] = f'Match date can not be after series end date.'
            return Response(error_response, status=400)

        previous_match = series.matches.first()
        if previous_match:
            teams = {previous_match.team_a, previous_match.team_b}
            if match.team_a in teams and match.team_b in teams:
                match.series = series
                match.save()
            else:
                error_response['invalid_teams'] = f'Can\'t add Match, previous teams are different. {teams}'
                return Response(error_response, status=400)

        return Response(f'received {pk=}, {series_id=}, series= {series}')


class GroundViewSet(ModelViewSet):
    serializer_class = GroundSerializer
    queryset = Ground.objects.all()


@api_view(['GET'])
@permission_classes(permission_classes=(IsVerifiedUser,))
def get_ground_with_most_matches(request):
    ground = Ground.objects.annotate(num_matches=Count('match')).order_by('-num_matches').first()
    serializer = GroundSerializer(ground, context={'request': request})
    return Response({'ground': serializer.data, 'match_count': ground.num_matches})

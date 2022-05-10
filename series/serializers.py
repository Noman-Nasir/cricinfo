from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Ground, Match, Series


class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

    def validate(self, data):
        if data['team_a'].id == data['team_b'].id:
            raise ValidationError('Both teams must have different id\'s.')
        if data['team_a'].name == data['team_b'].name:
            raise ValidationError('Both teams must have different name.')

        team_a_player_ids = set(data['team_a'].players.values_list('id', flat=True))
        team_b_player_ids = set(data['team_b'].players.values_list('id', flat=True))

        if not team_a_player_ids.isdisjoint(team_b_player_ids):
            common_players = team_a_player_ids.intersection(team_b_player_ids)
            raise ValidationError(
                f'One Player cannot play for two teams at the same time. Common players ids: {common_players}'
            )

        series = data['series']
        if series is not None:
            if data['match_date'] < series.start_date:
                raise ValidationError('Match date can not be before series start date.')
            if data['match_date'] > series.end_date:
                raise ValidationError('Match date can not be after series end date.')

            previous_match = series.matches.first()
            if previous_match:
                teams = {previous_match.team_a, previous_match.team_b}
                if data['team_a'] not in teams or data['team_b'] not in teams:
                    raise ValidationError('Can\'t add Match, previous teams are different. {teams}')

        return super(MatchSerializer, self).validate(data)

    def update(self, instance, validated_data):
        if instance.series and validated_data['series']:
            raise ValidationError(
                'Can\'t Update Match information when set to a Series'
            )
        return super(MatchSerializer, self).update(instance, validated_data)


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'matches', 'start_date', 'end_date']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise ValidationError('Start Date must come before End Date')

        return super(SeriesSerializer, self).validate(data)

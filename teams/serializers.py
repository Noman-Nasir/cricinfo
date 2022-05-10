from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    def validate_players(self, team_members):
        if len(team_members) < 12 or len(team_members) > 17:
            raise ValidationError('A Team must have at-least 12 members and at max 17 members')
        return team_members

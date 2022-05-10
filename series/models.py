from django.db import models

from teams.models import Team
from teams.models import Team
from teams.models import Team


class Ground(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    head_curator = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} Located at: {self.address}'


class Series(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'


class Match(models.Model):
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_b')
    match_date = models.DateField()

    venue = models.ForeignKey(Ground, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, related_name='matches')

    TEAM_A_WIN = 'TA'
    TEAM_B_WIN = 'TB'
    TIE = 'TI'
    NO_RESULT = 'NR'

    RESULT_CHOICES = [
        (TEAM_A_WIN, 'Team A Won'),
        (TEAM_B_WIN, 'Team B Won'),
        (TIE, 'Match was tied'),
        (NO_RESULT, 'No Result - Match was Abandoned.'),
    ]
    result = models.CharField(max_length=2, choices=RESULT_CHOICES, default=NO_RESULT)

    def __str__(self):
        return f'{self.team_a.name} vs {self.team_b.name} on {self.match_date}.'

from django.core.validators import MinValueValidator
from django.db import models


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField()
    date_of_birth = models.DateField()
    bio = models.TextField()
    address = models.CharField(max_length=200)

    BATTER = 'BA'
    BOWLER = 'BO'
    WICKETKEEPER = 'WK'
    ALLROUNDER = 'AR'

    ROLE_CHOICES = [
        (BATTER, 'Batter'),
        (BOWLER, 'Bowler'),
        (WICKETKEEPER, 'Wicket Keeper'),
        (ALLROUNDER, 'All Rounder'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=ALLROUNDER)

    LEFT_HANDED = 'LH'
    RIGHT_HANDED = 'RH'

    BATTING_STYLE_CHOICES = [
        (LEFT_HANDED, 'Left Handed'),
        (RIGHT_HANDED, 'Right Handed'),
    ]
    batting_style = models.CharField(max_length=2, choices=BATTING_STYLE_CHOICES, default=RIGHT_HANDED)

    LEFT_ARM_FAST = 'LF'
    LEFT_ARM_MEDIUM = 'LM'
    LEFT_ARM_OFFSPIN = 'LO'
    CHINAMAN = 'CM'
    RIGHT_ARM_FAST = 'RF'
    RIGHT_ARM_MEDIUM = 'RM'
    RIGHT_ARM_OFFSPIN = 'RO'
    RIGHT_ARM_LEGSPIN = 'RL'

    BOWLING_STYLE_CHOICES = [
        (LEFT_ARM_FAST, 'Left Arm FAST'),
        (LEFT_ARM_MEDIUM, 'Left Arm Medium'),
        (LEFT_ARM_OFFSPIN, 'Left Arm Offspin'),
        (CHINAMAN, 'Chinaman'),
        (RIGHT_ARM_OFFSPIN, 'Right Arm Offspin'),
        (RIGHT_ARM_LEGSPIN, 'Right Arm Legspin'),
        (RIGHT_ARM_MEDIUM, 'Right Arm Medium'),
        (RIGHT_ARM_FAST, 'Right Arm Fast'),
    ]
    bowling_style = models.CharField(max_length=2, choices=BOWLING_STYLE_CHOICES, default=RIGHT_ARM_FAST)
    icc_ranking = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'


class Team(models.Model):
    PAKISTAN = 'PAK'
    INDIA = 'IND'
    AUSTRALIA = 'AUS'
    SOUTH_AFRICA = 'SA'
    BANGLADESH = 'BAN'
    ENGLAND = 'ENG'
    SRILANKA = 'SL'
    WEST_INDIES = 'WI'
    ZIMBABWE = 'ZIM'
    NEW_ZEALAND = 'NZ'

    TEAM_CHOICES = [
        (PAKISTAN, 'PAKISTAN'),
        (INDIA, 'INDIA'),
        (AUSTRALIA, 'AUSTRALIA'),
        (SOUTH_AFRICA, 'SOUTH AFRICA'),
        (BANGLADESH, 'BANGLADESH'),
        (ENGLAND, 'ENGLAND'),
        (SRILANKA, 'SRILANKA'),
        (WEST_INDIES, 'WEST INDIES'),
        (ZIMBABWE, 'ZIMBABWE'),
        (NEW_ZEALAND, 'NEW ZEALAND'),
    ]
    name = models.CharField(max_length=3, choices=TEAM_CHOICES)
    players = models.ManyToManyField(to=Player, related_name='team_players')

    def __str__(self):
        return f'id:{self.id} Name:{self.name}'


class PlayerVisitCounter(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.player.id}: {self.player.first_name} {self.player.last_name} - {self.visit_count}'

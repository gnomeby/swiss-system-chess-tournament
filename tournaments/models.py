from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=200)
    register_date = models.DateTimeField('registration date')
    initial_rating = models.IntegerField()
    rating = models.IntegerField()
    fide_id = models.BigIntegerField('FIDE ID')
    fide_title = models.CharField(max_length=10)

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    players = models.ManyToManyField(Player)

class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    name = models.CharField(max_length=200)
    round_date = models.DateTimeField()

class Game(models.Model):
    GAME_STATUSES = (
        ('planned', 'planned'),
        ('finished', 'finished'),
        ('walkover', 'walkover'),
    )

    round = models.ForeignKey(Round)
    player = models.ForeignKey(Player, related_name="player_a")
    player_score = models.DecimalField(max_digits=4, decimal_places=1)
    opponent = models.ForeignKey(Player, related_name="player_b")
    opponent_score = models.DecimalField(max_digits=4, decimal_places=1)
    status = models.CharField(max_length=10,
                              choices=GAME_STATUSES,
                              default='planned')
    

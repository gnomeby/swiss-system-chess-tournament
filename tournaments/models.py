from django.db import models
from snippets.countries import CountryField

# Support CountryField for South
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^snippets\.countries\.CountryField"])

# Create your models here.
class Player(models.Model):
    FIDE_TITLES = (
        ('GM', 'Grandmaster'),
        ('IM', 'International Master'),
        ('FM', 'FIDE Master'),
        ('CM', 'Candidate Master'),
        ('WGM', 'Woman Grandmaster'),
        ('WIM', 'Woman International Master'),
        ('WFM', 'Woman FIDE Master'),
        ('WCM', 'Woman Candidate Master'),
    )
        
    name = models.CharField(max_length=200)
    country = CountryField()
    register_date = models.DateField('registration date', auto_now_add=True)
    initial_rating = models.IntegerField()
    rating = models.IntegerField()
    fide_id = models.BigIntegerField('FIDE ID')
    fide_title = models.CharField(max_length=10, choices=FIDE_TITLES)
    
    def save(self, *args, **kwargs):
        if self.id == None:
            self.rating = self.initial_rating
        super(Player, self).save(*args, **kwargs) # Call the "real" save() method.
        
    def __unicode__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    country = CountryField()
    city = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    players = models.ManyToManyField(Player)
    
    def __unicode__(self):
        return self.name
    
    def players_count(self):
        return self.players.count()


class Round(models.Model):
    tournament = models.ForeignKey(Tournament)
    name = models.CharField(max_length=200)
    round_date = models.DateField()

    def __unicode__(self):
        return self.tournament.name + " - " + self.name

class Game(models.Model):
    GAME_STATUSES = (
        ('planned', 'Planned'),
        ('finished', 'Finished'),
        ('walkover', 'Walkover'),
    )

    PLAYER_SCORES = (
        (0, '0'),
        (0.5, '0.5'),
        (1.0, '1'),
    )

    round = models.ForeignKey(Round)
    player = models.ForeignKey(Player, related_name="player_a")
    player_score = models.DecimalField(max_digits=4, decimal_places=1, default=0, choices=PLAYER_SCORES)
    opponent_score = models.DecimalField(max_digits=4, decimal_places=1, default=0, choices=PLAYER_SCORES)
    opponent = models.ForeignKey(Player, related_name="player_b")
    status = models.CharField(max_length=10,
                              choices=GAME_STATUSES,
                              default='planned')
    
    def __unicode__(self):
        return str(self.player) + " " + str(self.player_score) + ":" + str(self.opponent_score) + " " + str(self.opponent)

from django.db import models
from snippets.countries import CountryField

# Support CountryField for South
from south.modelsinspector import add_introspection_rules
from django.db.transaction import managed
add_introspection_rules([], ["^snippets\.countries\.CountryField"])

# Create your models here.
class Player(models.Model):
    FIDE_TITLES = (
        ('8 GM', 'Grandmaster'),
        ('7 IM', 'International Master'),
        ('5 FM', 'FIDE Master'),
        ('3 CM', 'Candidate Master'),
        ('6 WGM', 'Woman Grandmaster'),
        ('4 WIM', 'Woman International Master'),
        ('2 WFM', 'Woman FIDE Master'),
        ('1 WCM', 'Woman Candidate Master'),
        ('0 nt', 'no title'),
    )
    DEVELOPMENT_COEFFICIENT = (
        (None, 'Auto'),
        (30, '30'),
        (15, '15'),
        (10, '10'),
    )
            
    name = models.CharField(max_length=200)
    country = CountryField()
    register_date = models.DateField('registration date', auto_now_add=True)
    initial_rating = models.IntegerField()
    rating = models.IntegerField()
    rating_dev_coef = models.IntegerField(choices=DEVELOPMENT_COEFFICIENT, default=None, null=True)
    last_rating_calculation = models.DateField(null=True, default=None)
    fide_id = models.BigIntegerField('FIDE ID')
    fide_title = models.CharField(max_length=10, choices=FIDE_TITLES, default='0 nt')
    
    def save(self, *args, **kwargs):
        if self.id == None:
            self.initial_rating = self.rating
        super(Player, self).save(*args, **kwargs) # Call the "real" save() method.
        
    def __unicode__(self):
        return self.name


class Tournament(models.Model):
    BYE_SCORES = (
        (0.5, '0.5'),
        (1.0, '1.0'),
    )
        
    name = models.CharField(max_length=200)
    country = CountryField()
    city = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    players = models.ManyToManyField(Player)
    bye_score = models.DecimalField(max_digits=2, decimal_places=1, default=1, choices=BYE_SCORES)
    
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
    
    PLAYER_COLOR = (
        ('W', 'White'),
        ('B', 'Black'),
    )

    round = models.ForeignKey(Round)
    player = models.ForeignKey(Player, related_name="player_a")
    player_color = models.CharField(max_length=1,
                                      choices=PLAYER_COLOR,
                                      default='W')
    player_score = models.DecimalField(max_digits=4, decimal_places=1, default=0, choices=PLAYER_SCORES)
    opponent_score = models.DecimalField(max_digits=4, decimal_places=1, default=0, choices=PLAYER_SCORES)
    opponent_color = models.CharField(max_length=1,
                                      choices=PLAYER_COLOR,
                                      default='B')
    opponent = models.ForeignKey(Player, related_name="player_b", null=True, blank=True)
    status = models.CharField(max_length=10,
                              choices=GAME_STATUSES,
                              default='planned')
    
    def __unicode__(self):
        return str(self.player) + " " + str(self.player_score) + ":" + str(self.opponent_score) + " " + str(self.opponent)


# Bind model to SQL VIEW
class Tournament_Player_Score(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    score = models.DecimalField(max_digits=4, decimal_places=1)
    rating = models.IntegerField()
    fide_title = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    
    class Meta:
        managed = False
    
    def __unicode__(self):
        return str(self.player) + " " + str(self.score)

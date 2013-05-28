# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    
    def forwards(self, orm):
        query = """
            CREATE VIEW tournaments_tournament_player_score AS
            SELECT CONCAT(tournaments_round.tournament_id, ':', player_score.player_id) as id, tournaments_round.tournament_id, player_score.player_id, SUM(player_score.score) as score
                FROM tournaments_round
                    INNER JOIN tournaments_game_player_score as `player_score` 
                    ON (tournaments_round.id = player_score.round_id)
                GROUP BY tournaments_round.tournament_id, player_score.player_id
            ;
        """
        db.execute(query)
    
    def backwards(self, orm):
        query = """
            DROP VIEW tournaments_tournament_player_score;
        """
        db.execute(query)
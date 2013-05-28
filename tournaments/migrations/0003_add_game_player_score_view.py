# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    
    def forwards(self, orm):
        query = """
            CREATE VIEW tournaments_game_player_score AS
                SELECT id as game_id, round_id, player_id, player_score as score FROM tournaments_game
                UNION ALL
                SELECT id as game_id, round_id, opponent_id as player_id, opponent_score as score FROM tournaments_game WHERE opponent_id IS NOT NULL
            ;
        """
        db.execute(query)
    
    def backwards(self, orm):
        query = """
            DROP VIEW tournaments_game_player_score;
        """
        db.execute(query)
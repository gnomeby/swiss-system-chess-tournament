# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing default value
        db.execute("ALTER TABLE tournaments_player CHANGE fide_title fide_title VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0 nt'")
        
        db.execute("UPDATE tournaments_player SET fide_title = '8 GM' WHERE fide_title = 'GM'")
        db.execute("UPDATE tournaments_player SET fide_title = '7 IM' WHERE fide_title = 'IM'")
        db.execute("UPDATE tournaments_player SET fide_title = '5 FM' WHERE fide_title = 'FM'")
        db.execute("UPDATE tournaments_player SET fide_title = '3 CM' WHERE fide_title = 'CM'")
        db.execute("UPDATE tournaments_player SET fide_title = '6 WGM' WHERE fide_title = 'WGM'")
        db.execute("UPDATE tournaments_player SET fide_title = '4 WIM' WHERE fide_title = 'WIM'")
        db.execute("UPDATE tournaments_player SET fide_title = '2 WFM' WHERE fide_title = 'WFM'")
        db.execute("UPDATE tournaments_player SET fide_title = '1 WCM' WHERE fide_title = 'WCM'")
        db.execute("UPDATE tournaments_player SET fide_title = '0 nt' WHERE fide_title = 'nt'")

        query = """
            DROP VIEW tournaments_game_player_score;
        """
        db.execute(query)
        
        query = """
            CREATE VIEW tournaments_game_player_score AS
                SELECT id as game_id, round_id, player_id, player_score as score, player_color as color FROM tournaments_game
                UNION ALL
                SELECT id as game_id, round_id, opponent_id as player_id, opponent_score as score, opponent_color as color FROM tournaments_game WHERE opponent_id IS NOT NULL
            ;
        """
        db.execute(query)

        query = """
            DROP VIEW tournaments_tournament_player_score;
        """
        db.execute(query)
        
        query = """
            CREATE VIEW tournaments_tournament_player_score AS
            SELECT CONCAT(tournaments_round.tournament_id, ':', player_score.player_id) as id, 
                tournaments_round.tournament_id, player_score.player_id, SUM(player_score.score) as score,
                player.name, player.rating, 
                player.fide_title
                
                FROM tournaments_round
                    INNER JOIN tournaments_game_player_score as `player_score` 
                    ON (tournaments_round.id = player_score.round_id)
                    INNER JOIN tournaments_player as `player` 
                    ON (player.id = player_score.player_id)
                GROUP BY tournaments_round.tournament_id, player_score.player_id
            ;
        """
        db.execute(query)


    def backwards(self, orm):
        # Deleting field 'Game.player_color'
        db.execute("ALTER TABLE tournaments_player CHANGE fide_title fide_title VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'nt'")

        db.execute("UPDATE tournaments_player SET fide_title = 'GM' WHERE fide_title = '8 GM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'IM' WHERE fide_title = '7 IM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'FM' WHERE fide_title = '5 FM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'CM' WHERE fide_title = '3 CM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'WGM' WHERE fide_title = '6 WGM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'WIM' WHERE fide_title = '4 WIM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'WFM' WHERE fide_title = '2 WFM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'WCM' WHERE fide_title = '1 WCM'")
        db.execute("UPDATE tournaments_player SET fide_title = 'nt' WHERE fide_title = '0 nt'")
        
        query = """
            DROP VIEW tournaments_game_player_score;
        """
        db.execute(query)
        
        query = """
            CREATE VIEW tournaments_game_player_score AS
                SELECT id as game_id, round_id, player_id, player_score as score FROM tournaments_game
                UNION ALL
                SELECT id as game_id, round_id, opponent_id as player_id, opponent_score as score FROM tournaments_game
                    WHERE opponent_id IS NOT NULL
            ;
        """
        db.execute(query)
        
        query = """
            DROP VIEW tournaments_tournament_player_score;
        """
        db.execute(query)
        
        query = """
            CREATE VIEW tournaments_tournament_player_score AS
            SELECT CONCAT(tournaments_round.tournament_id, ':', player_score.player_id) as id, 
                tournaments_round.tournament_id, player_score.player_id, SUM(player_score.score) as score,
                player.name, player.rating, 
                case player.fide_title
                    when "GM"  then 8
                    when "IM"  then 7
                    when "WGM" then 6
                    when "FM"  then 5
                    when "WIM" then 4
                    when "CM"  then 3
                    when "WFM" then 2
                    when "WCM" then 1
                    else 0 
                    end as title_number
                
                FROM tournaments_round
                    INNER JOIN tournaments_game_player_score as `player_score` 
                    ON (tournaments_round.id = player_score.round_id)
                    INNER JOIN tournaments_player as `player` 
                    ON (player.id = player_score.player_id)
                GROUP BY tournaments_round.tournament_id, player_score.player_id
            ;
        """
        db.execute(query)        


    models = {
        u'tournaments.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_b'", 'null': 'True', 'to': u"orm['tournaments.Player']"}),
            'opponent_color': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': '1'}),
            'opponent_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_a'", 'to': u"orm['tournaments.Player']"}),
            'player_color': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '1'}),
            'player_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Round']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'planned'", 'max_length': '10'})
        },
        u'tournaments.player': {
            'Meta': {'object_name': 'Player'},
            'country': ('snippets.countries.CountryField', [], {'max_length': '2'}),
            'fide_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'fide_title': ('django.db.models.fields.CharField', [], {'default': "'0 nt'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_rating': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'register_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'tournaments.round': {
            'Meta': {'object_name': 'Round'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'round_date': ('django.db.models.fields.DateField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Tournament']"})
        },
        u'tournaments.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'bye_score': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '2', 'decimal_places': '1'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('snippets.countries.CountryField', [], {'max_length': '2'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tournaments.Player']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'tournaments.tournament_player_score': {
            'Meta': {'object_name': 'Tournament_Player_Score', 'managed': 'False'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Player']"}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Tournament']"})
        }
    }

    complete_apps = ['tournaments']
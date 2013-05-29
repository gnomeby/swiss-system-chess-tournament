# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    
    def forwards(self, orm):
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
    
    def backwards(self, orm):
        query = """
            DROP VIEW tournaments_tournament_player_score;
        """
        db.execute(query)

    models = {
        u'tournaments.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_b'", 'null': 'True', 'to': u"orm['tournaments.Player']"}),
            'opponent_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_a'", 'to': u"orm['tournaments.Player']"}),
            'player_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '4', 'decimal_places': '1'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Round']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'planned'", 'max_length': '10'})
        },
        u'tournaments.player': {
            'Meta': {'object_name': 'Player'},
            'country': ('snippets.countries.CountryField', [], {'max_length': '2'}),
            'fide_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'fide_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('snippets.countries.CountryField', [], {'max_length': '2'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tournaments.Player']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['tournaments']
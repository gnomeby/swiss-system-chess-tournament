# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.player_color'
        db.add_column(u'tournaments_game', 'player_color',
                      self.gf('django.db.models.fields.CharField')(default='W', max_length=1),
                      keep_default=False)

        # Adding field 'Game.opponent_color'
        db.add_column(u'tournaments_game', 'opponent_color',
                      self.gf('django.db.models.fields.CharField')(default='B', max_length=1),
                      keep_default=False)

        # Adding field 'Tournament.bye_score'
        db.add_column(u'tournaments_tournament', 'bye_score',
                      self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=2, decimal_places=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.player_color'
        db.delete_column(u'tournaments_game', 'player_color')

        # Deleting field 'Game.opponent_color'
        db.delete_column(u'tournaments_game', 'opponent_color')

        # Deleting field 'Tournament.bye_score'
        db.delete_column(u'tournaments_tournament', 'bye_score')


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
            'fide_title': ('django.db.models.fields.CharField', [], {'default': "'nt'", 'max_length': '10'}),
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
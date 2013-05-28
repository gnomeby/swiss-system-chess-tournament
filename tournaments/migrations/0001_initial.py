# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'tournaments_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('snippets.countries.CountryField')(max_length=2)),
            ('register_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('initial_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('fide_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('fide_title', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'tournaments', ['Player'])

        # Adding model 'Tournament'
        db.create_table(u'tournaments_tournament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('snippets.countries.CountryField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'tournaments', ['Tournament'])

        # Adding M2M table for field players on 'Tournament'
        m2m_table_name = db.shorten_name(u'tournaments_tournament_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm[u'tournaments.tournament'], null=False)),
            ('player', models.ForeignKey(orm[u'tournaments.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tournament_id', 'player_id'])

        # Adding model 'Round'
        db.create_table(u'tournaments_round', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Tournament'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('round_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'tournaments', ['Round'])

        # Adding model 'Game'
        db.create_table(u'tournaments_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Round'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_a', to=orm['tournaments.Player'])),
            ('player_score', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=1)),
            ('opponent_score', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=4, decimal_places=1)),
            ('opponent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_b', to=orm['tournaments.Player'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='planned', max_length=10)),
        ))
        db.send_create_signal(u'tournaments', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'tournaments_player')

        # Deleting model 'Tournament'
        db.delete_table(u'tournaments_tournament')

        # Removing M2M table for field players on 'Tournament'
        db.delete_table(db.shorten_name(u'tournaments_tournament_players'))

        # Deleting model 'Round'
        db.delete_table(u'tournaments_round')

        # Deleting model 'Game'
        db.delete_table(u'tournaments_game')


    models = {
        u'tournaments.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_b'", 'to': u"orm['tournaments.Player']"}),
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
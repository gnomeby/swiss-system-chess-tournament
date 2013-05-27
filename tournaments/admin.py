from django.contrib import admin
from tournaments.models import Player, Tournament, Round, Game
from django import forms
from django.utils.functional import curry
import math

from modeladmins import player
from modeladmins import tournament
from modeladmins import round

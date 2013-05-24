swiss-system-chess-tournament
=============================

The system is for helping judges to provide chess tournaments based on swiss system.

#### Requirements:
* Python 2.7
* Django 1.5.1

#### Features:
* Setup players
* Setup tournaments
* Direct link to creating rounds in list of tournaments
* View tournament information
* View round information

#### Problems:
* How to store players for game? One record or two record?

#### TODO:
* Disable edit/delete if player have one finished game
* Disable delete if tournament have any round
* Disable edit players if tournament have any round
* Validation tournament dates
* Validation round date
* Disable delete if round have one finished game
* Order players in forms
* Optimize queries

swiss-system-chess-tournament
=============================

The system is for helping judges to provide chess tournaments based on swiss system.

#### Requirements:
* Python 2.7
* Django 1.5.1
* South 0.8

#### Features:
* Setup players
* Setup tournaments
** Sort Players alphabetically in Inline model
** Direct link to creating rounds in list of tournaments
** Remove Tournament_Player caption
* Setup rounds
** InLine edit for Games, valudation score and status, Sort Players alphabetically
** Autopairing by rating, score

##### User UI:
* View tournament information
* View round information
* View players information
* View initial standing information

#### Problems:
* How to store players for game? One record or two record?

#### TODO:
* Disable edit/delete if player have one finished game
* Disable delete if tournament have any round
* Disable edit players if tournament have any round
* Validation tournament dates, players
* Validation round date
* Disable delete if round have one finished game
* Optimize queries
* Validation game players
* Allow game without opponent
* Show only Round table for tournament (not all rounds)
* Support 0.5 for bye
* Support leaved players
* Support colors, rating ordering

#### Most difficult places:
* Autopairing by rating during round creating
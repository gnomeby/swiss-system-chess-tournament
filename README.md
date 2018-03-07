swiss-system-chess-tournament
=============================

The system is for helping judges to provide chess tournaments based on swiss system.

#### Requirements:
* Python 2.7
* * MySQL support
* Django 1.5.1
* South 0.8

#### Used rules:
* [Swiss System Based on Rating (The Dutch System)](http://www.fide.com/fide/handbook.html?id=83&view=article)
* * Pairing ordering: Score->Rating->Title (GM-IM-WGM-FM-WIM-CM-WFM-WCM-no title)->Alphabetically (name first)
* [FIDE Title Regulations effective from 1 July 2013](http://www.fide.com/component/handbook/?id=163&view=article)
* [FIDE Rating Regulations effective from 1 July 2013](http://www.fide.com/fide/handbook.html?id=161&view=article)
* [FIDE Rating calculator](http://ratings.fide.com/calculator_rtd.phtml)

#### Features:
* Setup players
* * ELO rating recalculation
* Setup tournaments
* * Sort Players alphabetically in Inline model
* * Direct link to creating rounds in list of tournaments
* * Remove Tournament_Player caption
* * Defining bye points
* Setup rounds
* * Autopairing by score, rating, title and name
* * InLine edit for Games
* * * Validation score, players, color and status 
* * * Sort Players alphabetically

##### User UI:
* List tournaments
* View tournament information
* View round information
* View standing information

#### Problems:
* How to store players for game? One record or two record?


#### TODO:
* Use Buchholz system
* Initial rating calculator
* Rest Swiss system rules:
* * For odd players/byes/walkover
* * Remember floats in past rounds (B.5, B.6)
* * Backtracking

##### Admin:
* Player: Disable delete players if ones are assigned to tournament
* Tour: Disable edit/delete players if tournament has any round
* Tour: Disable delete tournament if one has any round
* Tour: Validation tournament dates
* Round: Validation round date
* Round: Disable delete if round have one finished game
* Round: Disable edit tournament
* Round: Disable add if players less than 2
* Round: Restore filter for tables after leaving add/edit actions
* Game: Refresh Players/Opponents by AJAX

##### User UI:
* Cache pages
* Rounds: Order games by white player names
* Minor: Link to player FIDE page


#### Most difficult places:
* Autopairing by rating during round creating

#### FAQ
##### Is it suitable for non Swiss system?
Yes. In general this system only helps pairing during round creation. 
You can change pairs manually to follow any kind of tournament except tournament that allows to have move
than one game for the same players. 

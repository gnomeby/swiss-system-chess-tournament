swiss-system-chess-tournament
=============================

The system is for helping judges to provide chess tournaments based on swiss system.

#### Requirements:
* Python 2.7
* Django 1.5.1
* South 0.8

#### Used rules:
* [Swiss System Based on Rating (The Dutch System)](http://www.fide.com/fide/handbook.html?id=83&view=article)
* * Pairing ordering: Score->Rating->Title (GM-IM-WGM-FM-WIM-CM-WFM-WCM-no title)->Alphabetically (name first)
* [FIDE Title Regulations effective from 1 July 2013](http://www.fide.com/component/handbook/?id=163&view=article)

#### Features:
* Setup players
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
* View tournament information
* View round information
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
* Show only Round table for tournament (not all rounds)
* Support colors
* Link to player fide page
* Correct ordering for 1 round, enum for titles
* Show only tournament players in game selects
* Filter by AJAX right side
* allow to not have apponent
* Disable add round if players less than 2
* Order games by white player names

#### Most difficult places:
* Autopairing by rating during round creating

#### FAQ
##### Is it suitable for non Swiss system
Yes. In general this system only helps pairing during round creation. 
You can change pairs manually to follow any kind of tournament. 
In this case the system will help you to show results.
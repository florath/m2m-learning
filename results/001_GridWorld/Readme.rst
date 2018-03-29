Run
===

* 001 - Limited gameplay (as in the original source)
* 002 - Limited gameplay; -25 reward when game ends
* 003 - Max score 10000 per game (which was never reached); -25 reward when game ends; no penalty
* 004 - Max score 10000 per game (which was never reached); -25 reward when game ends; penalty
* 005 - Max score 10000 per game; annealing_steps = 100000; tau = 0.0001; endE = 0.00000001
* 006 - same as 005; endE = 0

Planned
=======

* Decrease endE; either to something VERY low like 0.00000001 or even 0.
* Add an additional reward, if the end of game is reached (e.g. another 5000 points)
* Add penalties for
  - every non-sensible step (e.g. go up at the top of the game-board)
  - every step: this hopefully lowers the circles used by the hero.


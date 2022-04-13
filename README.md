# Perch

It's project where I create AI to evaluate checkers positions.

### Position.py

Contains class which handles storing and changing positions. Also have methods for checking if the move is valid and generating all possible moves.

This module is shared with other project: https://github.com/andreimek/ML (not sure if it's public)

### Perch.py

This module contains classes which represent players. 

Random_player - player which makes random valid move in each position

Perch1 - neural network which makes moves by evaluating each position (with some depth in the future) and choosing the best move.
Learning of this alghorithm will be performed by generating some population of players which will play with each other and survive/reproduce depending on their results

Perch2 - reinforcment learning alghorithm

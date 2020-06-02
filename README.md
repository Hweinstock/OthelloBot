# Othello Bot

## Description
An AI for the board game Othello. This program uses the minimax algorithm to search the game tree and attempt to pick the very best option for its move. The evaluation function is a weighted sum of a few common factors in othello gameplay that make a gameboard 'good' for a player. 

## Purpose 

This project was aimed towards exposing myself to the mini-max algorithm and learning about some of its optimizations, such as alpha-beta pruning. 

## Setup

This is a standalone python3 script, should be able to run it/use it as expected, however since it is a turtle application, make sure to make the program interactive with the `-i` argument.    
`python3 -i OthelloBot.py`

## Usage 

The program supports Human V.S Human, AI V.S Human, or AI V.S. AI. Modifying the `compMoveW` and `compMoveB` functions could allow anyone to insert their own AI and have it play the existing model. When playing V.S. the AI. the amount of time each turn took will be logged in chat. This time will decrease exponentially by lower the depth argument. 
  


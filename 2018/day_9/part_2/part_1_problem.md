# Problem Report: Marble Circle Game Simulation

## Objective
Simulate a marble placement game and determine the highest score among all players after all marbles have been placed.

## Context
Multiple players take turns placing numbered marbles into a circular arrangement according to specific rules. Players accumulate points under certain conditions. We need to find the winning player's final score.

## Input Format
The input is a single line containing:
- Number of players (integer)
- The value of the last marble to be placed (integer)

Example input: `463 players; last marble is worth 71787 points`

This means:
- **Number of players**: 463
- **Last marble value**: 71787

## Game Rules

### Initial Setup
- Marbles are numbered sequentially starting from 0
- Marble 0 is placed first and designated as the "current marble"
- Players take turns in order (player 1, 2, 3, ..., N, then back to player 1)
- All players start with a score of 0

### Standard Placement (when marble number is NOT a multiple of 23)
1. Place the new marble between the marbles that are 1 and 2 positions **clockwise** from the current marble
2. The newly placed marble becomes the new current marble

### Special Placement (when marble number IS a multiple of 23)
1. The current player **keeps** the marble (adds its value to their score) instead of placing it
2. The marble 7 positions **counter-clockwise** from the current marble is **removed** from the circle
3. The removed marble's value is **also added** to the current player's score
4. The marble immediately **clockwise** of the removed marble becomes the new current marble

### Circular Nature
- The marbles form a circle, so moving clockwise or counter-clockwise wraps around
- When there's only one marble, it is considered both clockwise and counter-clockwise from itself

## Expected Output
A single integer representing the highest score achieved by any player after all marbles (0 through the last marble value) have been processed.

## Example Walkthrough
For 9 players with last marble worth 25 points:
- Player 5 places marble 23 (multiple of 23), so they keep it (score: +23)
- They also remove marble 9 from the circle (score: +9)
- Player 5's total score: 32
- No other player scores in this short game
- **Winning score: 32**

## Additional Test Cases
- 10 players, last marble 1618: expected high score = **8317**
- 13 players, last marble 7999: expected high score = **146373**
- 17 players, last marble 1104: expected high score = **2764**
- 21 players, last marble 6111: expected high score = **54718**
- 30 players, last marble 5807: expected high score = **37305**

## Implementation Notes
- The circle needs efficient insertion and removal operations
- Need to track current marble position as marbles are added/removed
- Need to track scores for each player
- The game processes marbles numbered from 0 to the last marble value (inclusive)

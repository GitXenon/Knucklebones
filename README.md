# Cult of the Lamb's Knucklebones

Recreation in Python of the game

## How to play

- The game consists of two 3x3 boards, each belonging to their respective player.
- The players take turns. On a player's turn, they roll a single 6-sided die, and must place it in a column on their board. A filled column does not accept any more dice.
- Each player has a score, which is the sum of all the dice values on their board. The score awarded by each column is also displayed.
- If a player places multiple dice of the same value in the same column, the score awarded for each of those dice is multiplied by the number of dice of the same value in that column. e.g. if a column contains 4-1-4, then the score for that column is 4x2 + 1x1 + 4x2 = 17. Below is a multiplication table for reference and comparison:
  |Die value|1 die in the column|2 dice|3 dice|
  |---|---|---|---|
  |1 | 1 | 4 | 9|
  |2 | 2 | 8 | 18|
  |3 | 3 | 12 | 27|
  |4 | 4 | 16 | 36|
  |5 | 5 | 20 | 45|
  |6 | 6 | 24 | 54 |
- When a player places a die, all dice of the same value in the corresponding column of the opponent's board gets destroyed. Players can use this mechanic to destroy their opponent's high-scoring combos.
- The game ends when either player completely fills up their 3x3 board. The player with the higher score wins.

from enum import Enum

class GameState(Enum):
   NOT_STARTED = 0
   GAME_OVER = 1
   ROUND_ACTIVE = 2
   ROUND_DONE = 3
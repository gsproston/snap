# constants for the snap game

FPS = 144
INSTANTPLAY = False
if INSTANTPLAY:
  TURNTIME = 0
  AIMINCALLTIME = 0
else:
  TURNTIME = 1 # how long the turns take in seconds, must be > 1
  AIMINCALLTIME = 0.5 # min time before the AI can call snap
SUITS = ["diamonds","clubs","hearts","spades"]
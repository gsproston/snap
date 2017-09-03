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

# window constants
RATIOS = ["16:9","16:10","4:3"] # ratios
RES169 = [[1024,576],[1152,648],[1280,720],[1366,768],[1600,900],[1920,1080]]
RES1610 = [[1280,800],[1440,900],[1680,1050]]
RES43 = [[960,720],[1024,768],[1280,960],[1400,1050],[1440,1080],[1600,1200],[1856,1392]]
RESS = [RES169,RES1610,RES43] # holds various resolution options
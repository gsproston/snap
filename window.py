import pygame, sys
from pygame.locals import *
import constants as cs

# new flags set
# returns the new screen object
def resetFlags(fscreen,bwindow): 
  # gets monitor info, used when resizing
  wInfo = pygame.display.Info()
  if fscreen:
    w = wInfo.current_w
    h = wInfo.current_h
    if bwindow:
      flags = FULLSCREEN|NOFRAME
    else:
      flags = FULLSCREEN
  else:
    w = windowWidth
    h = windowHeight
    if bwindow:
      flags = NOFRAME
    else:
      flags = 0
  pygame.display.set_mode((w,h),flags)
  
def getRatio():
  return cs.RATIOS[ratind]
  
def getResolution():
  return cs.RESS[ratind][resind]

def init():
  global ratind, resind
  print("Initialising the display")
  # variables
  # deciding on a square window for this card game
  windowWidth = 800
  windowHeight = 800
  flags = 0
  # menu variables
  fscreen = False # fullscreen
  bwindow = False # borderless
  ratind = 0 # index of the ratio menu
  resind = 0 # index of the resolution menu
  # ratios and resolutions can be found in constants

  # init screen
  screen = pygame.display.set_mode((windowWidth, windowHeight),flags)
  pygame.display.set_caption("Snap")
  screen.fill(Color(255,255,255))
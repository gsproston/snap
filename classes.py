# this file holds the Card and Player classes

import random
import pygame # used for the Display class set up
from pygame.locals import *
from constants import FPS # use to determine fade speed of menus

class Card:
  def __init__(self,suit,number,imgind):
    self.SUIT = suit # constant
    self.NUMBER = number # constant
    self.imgind = imgind # index of the image in cardImages
    self.initRot()
   
  # card gets a new rotation
  def initRot(self):
    self.rot = -2 + random.random()*4 # random rotation to encourage variety
  
  # converts card number to card rank in string format
  # example: 12 => "queen"
  def num2rank(self):
    if self.NUMBER == 1:
      return "ace"
    elif self.NUMBER == 11:
      return "jack"
    elif self.NUMBER == 12:
      return "queen"
    elif self.NUMBER == 13:
      return "king"
    else:
      return str(self.NUMBER)
  
  # returns the full name of a card
  # eg "queen of clubs"
  def fullName(self):
    return "%s of %s" % (self.num2rank(),self.SUIT)

class Player:
  def __init__(self,ind):
    self.facedown = [] # first element is the bottom of the pile
    self.faceup = [] # first element is the bottom of the pile
    self.knockedOut = False # boolean representing if the player is still in the game
    self.IND = ind # used to refer to index in Players list
    self.CALLCHANCE = 0.75 # percentage chance at which player will call snap per second
    self.FALSECALLCHANCE = 0.1 # percentage chance the player will call snap incorrectly per second
    
  # player turns over their faceup pile to facedown
  def flipPile(self):
    self.facedown = self.faceup[:]
    self.facedown.reverse()
    self.faceup[:] = []
  
  # returns the top Card of the face up pile
  def getTopCard(self):
    if len(self.faceup) == 0:
      print("\nWARNING: TOP CARD REQUESTED FROM EMPTY PILE\n")
      return None
    else:
      return self.faceup[len(self.faceup)-1]
  
  # simulates the player's turn
  def turn(self):
    if not self.knockedOut:
      if len(self.facedown) == 0:
        if len(self.faceup) == 0: # player is knocked out, shouldn't be called here
          print("\tWARNING: KNOCK OUT OCCURED IN TURN FUNCTION")
          print("\tCONTINUING GAME REGARDLESS")
          self.knockedOut = True
          return
        else: # faceup pile becomes the facedown pile
          print("\tface down pile empty, swapping piles")
          self.flipPile()        
      self.faceup.append(self.facedown.pop())  
      self.getTopCard().initRot() # redo card rotation
      print("\tface down pile: %d" % len(self.facedown))
      print("\tface up pile: %d" % len(self.faceup))
      print("\ttop card is the %s" % (self.getTopCard().fullName()))      
      
  # empties the player's face up pile
  # this could be an elimination condition, so check for that
  def emptyFaceup(self):
    self.faceup[:] = []
    # check if eliminated
    if len(self.facedown) == 0:
      print("Player %d has no remaining cards! Eliminating!" % (self.IND+1))
      self.knockedOut = True
  
  # add a player's face up piles to the face down pile
  # input is the player whose pile is being added  
  def addPile(self,pp):
    print("\tplayer %d takes %d cards from player %d" % (self.IND+1,len(pp.faceup),pp.IND+1))
    # reverse the face up piles
    pp.faceup.reverse 
    pp.faceup.extend(self.facedown)
    self.facedown = pp.faceup[:]
    # empty the remaining face up piles
    pp.emptyFaceup()
    
  # add pool to the face down pile
  # input is the pool
  def addPool(self,pool):
    print("\tplayer %d takes %d cards from the pool" % (self.IND+1,len(pool)))
    pool.reverse
    pool.extend(self.facedown)
    self.facedown = pool[:]
    # empty the remaining face up piles
    
class Menu:
  def __init__(self,name):
    self.NAME = name
    self.buttons = []
    # font sizes and type face
    self.titleSize = 42 # also title height 
    self.textSize = 30 # also button height
    self.titleFont = pygame.font.SysFont("helvetica",self.titleSize)
    self.textFont = pygame.font.SysFont("helvetica",self.textSize)
    # transparency settings
    self.alpha = 0
    self.targetAlpha = 0
    self.fspeed = 5 # speed at which menu fades in and out
    # dimensions
    self.w = 200
    self.h = 100
    self.gap = 20 # space between buttons
    
  # from the mouse movement, finds if the mouse is now on a button
  def movement(self,x,y):
    y = y - self.gap*2 - self.titleSize
    for i in range(0,len(self.buttons)):
      if y <= self.textSize and y > 0:
        self.buttons[i].colour = Color(80,80,80)
      else:
        self.buttons[i].colour = Color(0,0,0)
      y = y - self.gap - self.textSize
  
  # from the mouse click, finds the button that was clicked and executes its command
  def click(self,x,y):
    y = y - self.gap*2 - self.titleSize
    if y < 0:
      # click registered on the title, exit
      return
    for i in range(0,len(self.buttons)):
      if y <= self.textSize and y > 0:
        self.buttons[i].execute()
        return
      y = y - self.gap - self.textSize
    
  def addButton(self,button):
    self.buttons.append(button)
    
  def addCommand(self,bname,command):
    for b in self.buttons:
      if b.NAME == bname:
        b.addCommand(command)
        return
    
  def calcHeight(self):
    h = self.titleSize + self.gap
    for b in self.buttons:
      h = h + self.gap + self.textSize
    self.h = h
    
  def getDims(self):
    return (self.w,self.h)
    
  # returns the menu surface
  def getSurface(self):
    surf = pygame.Surface((self.w,self.h))
    surf.fill(pygame.Color(255,255,255))
    # add in the title
    titleSurf = self.titleFont.render(self.NAME,4,Color(0,0,0))
    surf.blit(titleSurf,((self.w-titleSurf.get_width())/2.0,0))
    # add in the buttons
    cumh = self.titleSize+self.gap*2 # double gap between title and buttons
    for i in range(0,len(self.buttons)):
      buttonSurf = self.textFont.render(self.buttons[i].NAME,4,self.buttons[i].colour)
      surf.blit(buttonSurf,((self.w-buttonSurf.get_width())/2.0,cumh))
      cumh = cumh + self.textSize + self.gap
    surf.set_alpha(self.alpha)
    return surf
      
  def show(self): # show the menu
    self.targetAlpha = 255
    for b in self.buttons:
      b.show()
      
  def hide(self): # hide the menu
    self.targetAlpha = 0
    for b in self.buttons:
      b.hide()
      
  def fade(self): # fade the menu in or out
    if self.alpha > self.targetAlpha:
      self.alpha = max(self.targetAlpha,self.alpha-self.fspeed)
    elif self.alpha < self.targetAlpha:
      self.alpha = min(self.targetAlpha,self.alpha+self.fspeed)
    for b in self.buttons:
      b.fade(self.fspeed)
      
  def isHidden(self): # return True if all buttons are hidden
    for b in self.buttons:
      if b.alpha > 0:
        return False
    return True
  
  def isShown(self): # returns true if all buttons are show
    for b in self.buttons:
      if b.alpha < 255:
        return False
    return True
    
class Button:
  def __init__(self,name,command):
    self.NAME = name
    self.alpha = 0
    self.targetAlpha = 0
    self.command = command
    self.colour = Color(0,0,0)
  
  def addCommand(self,command):
    self.command = command
  
  # runs when the button is clicked
  def execute(self):
    print("%s button has been pressed" % self.NAME)
    # only execute if the command variable is set
    if self.command:
      self.command()
    else:
      print("WARNING: %s button has no command" % (self.NAME))
    
  def show(self):
    self.targetAlpha = 255
    
  def hide(self):
    self.targetAlpha = 0
    
  def fade(self,fspeed):
    if self.alpha > self.targetAlpha:
      self.alpha = max(self.targetAlpha,self.alpha-fspeed)
    elif self.alpha < self.targetAlpha:
      self.alpha = min(self.targetAlpha,self.alpha+fspeed)
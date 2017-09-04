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
    self.titleFont = pygame.font.SysFont("helvetica",self.titleSize)
    # transparency settings
    self.alpha = 0
    self.targetAlpha = 0
    self.fspeed = 5 # speed at which menu fades in and out
    # dimensions
    self.w = 200
    self.h = 100
    self.gap = 16 # space between buttons
    
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
      b = self.buttons[i]
      buttonSurf = b.getSurface()
      surf.blit(buttonSurf,((self.w-buttonSurf.get_width())/2.0,cumh))
      # if a drop down box is active, do not display lower buttons
      if isinstance(b,Dropdown) and b.opened:
        break
      cumh = cumh + b.textSize + self.gap
    surf.set_alpha(self.alpha)
    return surf
    
  # from the mouse movement, finds if the mouse is now on a button
  def movement(self,x,y):
    y = y - self.gap*2 - self.titleSize
    for i in range(0,len(self.buttons)):
      if y <= self.buttons[i].textSize and y > 0:
        self.buttons[i].onColour()
      else:
        self.buttons[i].offColour()
      y = y - self.gap - self.buttons[i].textSize
  
  # from the mouse click, finds the button that was clicked and executes its command
  def click(self,x,y):
    y = y - self.gap*2 - self.titleSize
    if y < 0:
      # click registered on the title, exit
      return
    for i in range(0,len(self.buttons)):
      b = self.buttons[i]
      if y <= b.textSize and y > 0:
        b.execute()
        return
      # if a dropdown box is active, make sure buttons below cannot be pressed
      if isinstance(b,Dropdown) and b.opened:
        return
      y = y - self.gap - b.textSize
    
  def addButton(self,bname,bcom):
    self.buttons.append(Button(bname,bcom,self))
    
  def addDropdown(self,bname,bopt,bcom):
    self.buttons.append(Dropdown(bname,bopt,bcom,self))
    
  def addCommand(self,bname,command):
    for b in self.buttons:
      if b.NAME == bname:
        b.addCommand(command)
        return
    
  def calcDims(self):
    h = self.titleSize + self.gap
    dh = 0 # used to track additional height from dropdown boxes
    for b in self.buttons:
      h = h + self.gap + b.textSize
      if isinstance(b,Dropdown):
        dh = b.dh
      else:
        dh = dh - self.gap - b.textSize
    self.h = h + max(0,dh)
    # now find the width
    titleSurf = self.titleFont.render(self.NAME,4,Color(0,0,0))
    w = titleSurf.get_width()
    for b in self.buttons:
      bsurf = b.getSurface()
      w = max(bsurf.get_width(),w)
    self.w = w
    
  def getDims(self):
    return (self.w,self.h)
      
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
      
  def isFaded(self): # return True if menu is completely faded
    for b in self.buttons:
      if not b.isFaded():
        return False
    return True
    
class Button:
  def __init__(self,name,command,menu):
    self.NAME = name
    self.MENU = menu
    self.alpha = 0
    self.targetAlpha = 0
    self.command = command
    self.colour = Color(0,0,0)
    self.textSize = 24 # also button height
    self.textFont = pygame.font.SysFont("helvetica",self.textSize)
    
  def getSurface(self):
    surf = self.textFont.render(self.NAME,4,self.colour)
    surf.set_alpha(self.alpha)
    return surf
    
  def onColour(self):
    self.colour = Color(80,80,80)
    
  def offColour(self):
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
      
  def isFaded(self):
    return (self.alpha == self.targetAlpha)

# slight alteration of the button class
class Dropdown(Button):
  def __init__(self,name,options,command,menu):
    Button.__init__(self,name,command,menu)
    self.options = options
    self.dropAlpha = 0
    self.dropTargetAlpha = 0
    self.opened = False
    self.dw = 200
    self.dh = 100
    self.calcDims()
    
  def getSurface(self):
    nameSurf = self.textFont.render("%s: " % self.NAME,4,Color(0,0,0))
    selectedSurf = self.textFont.render(self.options[0],4,self.colour)
    if self.opened:
      # get the drop down menu
      dropSurf = pygame.Surface((self.dw,self.dh))
      dropSurf.fill(Color(255,255,255))
      # add in all the options
      y = 0 # keeps track of where to blit the next option
      for i in range(1,len(self.options)):
        optSurf = self.textFont.render(self.options[i],4,self.colour)
        dropSurf.blit(optSurf,(0,y))
        y = y + self.MENU.gap + self.textSize
      # create main surface and blit everything
      surf = pygame.Surface((nameSurf.get_width()+self.dw,self.textSize+self.MENU.gap+dropSurf.get_height()))
      surf.fill(Color(255,255,255))
      surf.blit(nameSurf,(0,0))
      surf.blit(selectedSurf,(nameSurf.get_width(),0))
      surf.blit(dropSurf,(nameSurf.get_width(),self.textSize+self.MENU.gap))
    else: 
      surf = pygame.Surface((nameSurf.get_width()+self.dw,self.textSize))
      surf.fill(Color(255,255,255))
      surf.blit(nameSurf,(0,0))
      surf.blit(selectedSurf,(nameSurf.get_width(),0))
    surf.set_alpha(self.alpha)
    return surf
    
  def execute(self):
    if self.opened:
      self.close()
    else:
      self.open()
    
  def calcDims(self):
    self.dh = (self.MENU.gap+self.textSize) * (len(self.options)-1)
    w = 0
    for opt in self.options:
      optSurf = self.textFont.render(opt,4,self.colour)
      w = max(optSurf.get_width(),w)
    self.dw = w
    
  def open(self):
    self.dropTargetAlpha = 255
    self.opened = True
    
  def close(self):
    self.dropTargetAlpha = 0
    self.opened = False
    
  def fade(self,fspeed):
    Button.fade(self,fspeed)
    if self.dropAlpha > self.dropTargetAlpha:
      self.dropAlpha = max(self.dropTargetAlpha,self.dropAlpha-fspeed)
    elif self.dropAlpha < self.dropTargetAlpha:
      self.dropAlpha = min(self.dropTargetAlpha,self.dropAlpha+fspeed)
      
  def isFaded(self):
    return (self.dropAlpha == self.dropTargetAlpha and Button.isFaded(self))
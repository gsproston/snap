#Author: George Sproston
#Created: 2017/07/12
#Updated: 2017/07/19
#Snap card game

from random import shuffle
import random
import platform
import sys        
import pygame
from pygame.locals import *

pygame.init()

def draw(): #called when screen needs to be updated
  pygame.display.flip()
    
def wresize(): #screen is resized, recalculate some variables
  global cxpos,cypos
  cxpos = int(screen.get_width()/2)
  cypos = int(screen.get_height()/2)

def resetFlags(): #new flags set
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
  screen = pygame.display.set_mode((w,h),flags)
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
# converts card number to card rank
# example: 12 => "queen"
def num2rank(number):
  if number == 1:
    return "ace"
  elif number == 11:
    return "jack"
  elif number == 12:
    return "queen"
  elif number == 13:
    return "king"
  else:
    return str(number)
  
# returns the full card name of a Card 
# example: "queen of spades"
def fullCardName(card):
  return "%s of %s" % (num2rank(card.number),card.suit)

# returns the sum of the elements in a list
def sumList(l):
  tot = 0
  for num in l:
    tot = tot + num
  return tot

def printTopCards(players):
  for i in range(0,len(players)):
    if players[i].knockedOut:
      continue
    if len(players[i].faceup) == 0:
      print("\tplayer %d has no face up cards" % (i+1))
    else:
      print("\tplayer %d has the %s" % (i+1,fullCardName(players[i].getTopCard())))

# checks if a player has done a good snap
# inputs are list of all players, and the index of the Player that called snap
# returns boolean if there is only one person with cards or not
def checkSnap(players,callind):
  print("\nPlayer %d has called SNAP!" % (callind+1))
  # check all faceup piles against other faceup piles
  compList = [] # list of comparisons
  number = 0
  printTopCards(players) # print out everyone's top cards
  for i in range(0,len(players)):
    if len(players[i].faceup) == 0: # empty faceup pile, check next player
      compList.append(-1)
      continue
    number = players[i].getTopCard().number
    if len(compList) == 0: # empty compList, add
      compList.append(number)
      continue
    if number in compList: 
      
      # matching numbers, correct snap!
      pc = players[callind] # player who called snap
      # get the two players whose top cards match
      p1 = players[i]
      p2ind = compList.index(number) # index of second player
      p2 = players[p2ind]
      print("\tplayers %d and %d have matching cards!" % (p2ind+1,i+1))
      print("\tadding %d cards to the bottom of player %d's face down pile\n" % (len(p1.faceup)+len(p2.faceup),callind+1))
      choice = random.getrandbits(1) # randomly add one pile first
      # reverse the face up piles
      p1.faceup.reverse 
      p2.faceup.reverse
      if choice:
        p1.faceup.extend(pc.facedown)
        p2.faceup.extend(p1.faceup)
        pc.facedown = p2.faceup[:]
      else:
        p2.faceup.extend(pc.facedown)
        p1.faceup.extend(p2.faceup)
        pc.facedown = p1.faceup[:]
      # empty the remaining face up piles
      p1.faceup[:] = []
      p2.faceup[:] = []
      
      # check if either player is knocked out
      for p in [p1,p2]:
        if len(p.facedown) == 0:
          # no remaining cards in either pile, knock out
          print("Player %d has no remaining cards! Eliminating!" % (players.index(p)+1))
          p.knockedOut = True
          
          # check if the game should finish
          tot = 0 # number of players still playing
          winner = -1
          for j in range(0,len(players)):
            if not players[j].knockedOut:
              winner = j
              tot = tot + 1
          print("%d players remain!\n" % tot)
          if tot <= 1: # end the game!
            return True
      return False
    
    else:
      compList.append(number)
  # only reaches here if no two top cards match
  print("\tno players have matching cards, bad snap\n")
  return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#             CLASSES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Card:
  def __init__(self,suit,number):
    self.suit = suit
    self.number = number

class Player:
  def __init__(self):
    self.facedown = [] # first element is the bottom of the pile
    self.faceup = [] # first element is the bottom of the pile
    self.knockedOut = False # boolean representing if the player is still in the game
    
  # player turns over their faceup pile to facedown
  def flipPile(self):
    self.facedown = self.faceup[:]
    self.facedown.reverse()
    self.faceup = []
  
  def getTopCard(self):
    if len(self.faceup) == 0:
      print("\nWARNING: TOP CARD REQUESTED FROM EMPTY PILE\n")
      return None
    else:
      return self.faceup[len(self.faceup)-1]
  
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
      print("\tface down pile: %d" % len(self.facedown))
      print("\tface up pile: %d" % len(self.faceup))
      print("\ttop card is the %s" % fullCardName(self.getTopCard()))
    
if __name__ == "__main__":
  #gets monitor info, used when resizing
  wInfo = pygame.display.Info()

  #variables
  shutdown = False
  windowWidth = 1024
  windowHeight = 576
  flags = 0
  #menu variables
  fscreen = False #fullscreen
  bwindow = False #borderless
  ratios = ["16:9","16:10","4:3"] #ratios
  ress = [[],[],[]] #holds various resolution options
  res169 = [[1024,576],[1152,648],[1280,720],[1366,768],[1600,900],[1920,1080]]
  res1610 = [[1280,800],[1440,900],[1680,1050]]
  res43 = [[960,720],[1024,768],[1280,960],[1400,1050],[1440,1080],[1600,1200],[1856,1392]]
  ress[0] = res169
  ress[1] = res1610
  ress[2] = res43

  #init screen
  screen = pygame.display.set_mode((windowWidth, windowHeight),flags)
  cxpos = int(screen.get_width()/2)
  cypos = int(screen.get_height()/2)
  screen.fill(Color(255,255,255))
  print("Display up and running")
  
  clock = pygame.time.Clock()
  FPS = 144

  draw()
  
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #          INITIALISATIONS
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # initialise the deck
  suits = ["diamonds","clubs","hearts","spades"]
  deck = [] # a list of Card objects
  for suit in suits:
    for number in range(1,14):
      deck.append(Card(suit,number))
  
  # pre game initialisations
  play = 1 # game continues until this is 0
  waitCount = 0 # how long the program waits to play a turn
  pool = []
  players = [] # list of active players in the game
  
  print("Initialisation complete")
  print("Entering game loop\n")
  
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #          MAIN GAME LOOP
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  while(play):

    # initialisations for each game of snap
    winner = 0 # continue game until there's a winner
    # empty the lists again
    pool[:] = [] 
    players[:] = [] 
    numplayers = 4 # must be between 2 and 6
    for i in range(0,numplayers):
      players.append(Player())
    playerCounter = 0 # keeps track of whose turn it is
    
    # deal the cards
    shuffle(deck) # shuffle first
    for card in deck:
      players[playerCounter].facedown.append(card)
      playerCounter = (playerCounter+1) % numplayers
    playerCounter = 0 # need to reinitialise this

    while(not winner):
      
      # check for events first, my dog
      for event in pygame.event.get(): #runs when an event occurs
        if event.type == QUIT: #quit called
          play = 0
          winner = -1
        
        elif event.type == KEYDOWN: #key has been pressed
          if pygame.key.get_pressed()[pygame.K_ESCAPE]: # quit the game
            play = 0
            winner = -1
          elif pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_RETURN]: # player has snapped!
            if checkSnap(players,0):
              winner = 1
              
      if waitCount > FPS:
      #if True: # use this for instant play
        waitCount = 0
        print("Player %d playing" % (playerCounter+1))
        players[playerCounter].turn() # player does their turn
          
        # increment playerCounter
        playerCounter = (playerCounter+1) % numplayers
        while players[playerCounter].knockedOut:
          playerCounter = (playerCounter+1) % numplayers
        
      waitCount = waitCount + 1
      clock.tick(FPS) # update x times a second
      
    # game ended            
    print("")
    if winner > 0:
      print("Player %d wins!" % winner)
    else:
      print("No winner!")
      
    # do you want to play again?
    play = 0

  #main loop ends, exit
  pygame.quit()    

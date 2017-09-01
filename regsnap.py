from classes import Card, Player
import constants as cs
import random # used for shuffling
import sys        
import pygame
from pygame.locals import *
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def loadImages():
  # this should only be called once!
  # images must be global to be drawn
  # images are also constant
  global cardBackImage, cardImages    

  # load in images
  print("Loading images")
  cardBackImage = pygame.image.load("./images/cardBack.png")
  cardImages = []
  for i in range(1,14):
    for j in ["diamonds","clubs","hearts","spades"]:
      cardImages.append(pygame.image.load("./images/%d%s.png" % (i,j)))
      
  # scale images because god damn they're huge
  scaleImages(0.2)
        
def scaleImages(scale): # smoothly scales all images according to some input
  global cardBackImage, cardImages # get the images
  cardBackImage = pygame.transform.smoothscale(cardBackImage,(int(cardBackImage.get_width()*scale),int(cardBackImage.get_height()*scale)))
  for i in range(0,len(cardImages)):
    img = cardImages[i]
    cardImages[i] = pygame.transform.smoothscale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))

def draw(players,pool): #called when the whole screen needs to be updated
  screen = pygame.display.get_surface()
  screen.fill(Color(255,255,255)) # reset screen
  # face down piles always to the left
  # face up piles always to the right
  for p in players:
    if p.IND == 0:
      # first draw the face down pile
      for card in p.facedown:
        screen.blit(pygame.transform.rotozoom(cardBackImage,card.rot,1),(260,596))
      # now draw the face up pile
      for card in p.faceup:
        screen.blit(pygame.transform.rotozoom(cardImages[card.imgind],card.rot,1),(414,596))
        
    elif p.IND == 1:
      # first draw the face down pile
      for card in p.facedown:
        screen.blit(pygame.transform.rotozoom(cardBackImage,270+card.rot,1),(28,260))
      # now draw the face up pile
      for card in p.faceup:
        screen.blit(pygame.transform.rotozoom(cardImages[card.imgind],270+card.rot,1),(28,414))

    elif p.IND == 2:
      # first draw the face down pile
      for card in p.facedown:
        screen.blit(pygame.transform.rotozoom(cardBackImage,180+card.rot,1),(414,28))
      # now draw the face up pile
      for card in p.faceup:
        screen.blit(pygame.transform.rotozoom(cardImages[card.imgind],180+card.rot,1),(260,28))

    else:
      # first draw the face down pile
      for card in p.facedown:
        screen.blit(pygame.transform.rotozoom(cardBackImage,90+card.rot,1),(596,414))
      # now draw the face up pile
      for card in p.faceup:
        screen.blit(pygame.transform.rotozoom(cardImages[card.imgind],90+card.rot,1),(596,260))   

  # display the snap pool  
  for card in pool:
    screen.blit(pygame.transform.rotozoom(cardImages[card.imgind],card.rot,1),(337,312))  
    
  pygame.display.flip()

# simply prints out the names of all the cards on top of all the face up piles
def printPiles(players):
  for i in range(0,len(players)):
    if players[i].knockedOut or len(players[i].faceup) == 0:
      continue
    print("\tplayer %d has the %s" % (i+1,players[i].getTopCard().fullName()))  

# simply returns whether there is a good snap or not
def isSnap(players):
  topNumbers = []
  for i in range(0,len(players)):
    # skip player if they are knocked out or have no face up pile
    if players[i].knockedOut or len(players[i].faceup) == 0:
      continue
    # get top card number
    number = players[i].getTopCard().NUMBER
    if number in topNumbers: # good snap!
      return True
    else: # otherwise add the number to the list
      topNumbers.append(number)
  return False

# simply returns whether there is a good snap pool or not
def isSnapPool(players,pool):
  if len(pool) == 0: # exit if no pool
    return False
  poolnum = pool[len(pool)-1].NUMBER
  for i in range(0,len(players)):
    # skip player if they are knocked out or have no face up pile
    if players[i].knockedOut or len(players[i].faceup) == 0:
      continue
    # get top card number
    number = players[i].getTopCard().NUMBER
    if number == poolnum: # good snap!
      return True
  return False
    
# looks at all face up piles
# returns a list of players with matching piles
def matchingPiles(players):
  matchingPlayers = []
  for i in range(0,len(players)-1):
    # skip player if they are knocked out or have no face up pile or are already in the list
    if players[i].knockedOut or len(players[i].faceup) == 0 or players[i] in matchingPlayers:
      continue
    # cycle through the remaining players
    for j in range(i+1,len(players)):
      # skip player if they are knocked out or have no face up pile or are already in the list
      if players[j].knockedOut or len(players[j].faceup) == 0 or players[j] in matchingPlayers:
        continue
      if players[i].getTopCard().NUMBER == players[j].getTopCard().NUMBER:
        # numbers match! 
        matchingPlayers.append(players[i])
        matchingPlayers.append(players[j])
  return matchingPlayers      

# looks at all face up piles
# returns list of players whose cards match the pool
def matchingPool(players,pool):
  poolnum = pool[len(pool)-1].NUMBER
  matchingPlayers = []
  for p in players:
    # skip player if they are knocked out or have no face up pile
    if p.knockedOut or len(p.faceup) == 0:
      continue
    if p.getTopCard().NUMBER == poolnum:
      matchingPlayers.append(p)
  return matchingPlayers

# checks if a player has done a good snap
# inputs are list of all players, and the index of the Player that called snap
# returns boolean if there is a good snap
def checkSnap(players,callind):
  print("\nPlayer %d has called SNAP!" % (callind+1))
  printPiles(players)
  matchingPlayers = matchingPiles(players)
  
  if len(matchingPlayers) == 0:
    # bad snap
    print("\tbad snap\n")
    return False
  else:
    # good snap
    print("\tgood snap")
    pc = players[callind] # player who called snap
    # cycle through the players whose top cards match
    for pp in matchingPlayers:
      pc.addPile(pp)
    print("")
    return True
  
# checks if a player has done a good snap against the snap pool
# inputs are list of all players, and the index of the Player that called snap pool
# returns boolean if snap pool called correctly
def checkSnapPool(players,pool,callind):
  print("\nPlayer %d has called SNAP POOL!" % (callind+1))
  if len(pool) == 0: # empty pool
    print("\tpool empty, bad snap pool\n")
    return False
  matchingPlayers = matchingPool(players,pool)
  
  if len(matchingPlayers) == 0:
    # bad snap
    print("\tbad snap pool\n")
    return False
  else:
    # good snap
    print("\tgood snap pool")
    pc = players[callind] # player who called snap
    pc.addPool(pool)
    # cycle through the players whose top cards match
    for pp in matchingPlayers:
      pc.addPile(pp)
    print("")
    return True

# called when a bad snap occurs
# the player's face up pile is added to the pool
def badSnap(player,pool):
  if len(player.faceup) == 0:
    print("\tno face up cards available to add the pool")
    return pool # pool does not change
  print("\tadding %d cards to the pool" % len(player.faceup))
  pool.extend(player.faceup) # adding to the pool
  player.emptyFaceup() # empty the player's face up pile
  print("\tpool now has %d cards" % len(pool))
  print("\tthe top card is the %s" % (pool[len(pool)-1].fullName()))
  return pool
    
# returns the number of players that are not knocked out
# used to check if the game should end
def playersLeft(players):
  tot = 0
  for p in players:
    if not p.knockedOut:
      tot = tot + 1
  return tot

# checks if there is a winner
# returns the player number if there is,
# otherwise returns 0
def checkWinner(players):
  if playersLeft(players) == 1:
    for i in range(0,len(players)):
      if not players[i].knockedOut:
        return (i+1)
  return 0
    
def start():
  loadImages()  
  clock = pygame.time.Clock()
  
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #          INITIALISATIONS
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # initialise the deck
  deck = [] # a list of Card objects
  imgind = 0 # used to find images of cards in cardImages
  for number in range(1,14):
    for suit in cs.SUITS:
      deck.append(Card(suit,number,imgind))
      imgind = imgind + 1
  
  # pre game initialisations
  play = 1 # game continues until this is 0
  waitCount = 0 # how long the program waits to play a turn
  snap = False # true if there is a snap on the table
  snapPool = False # true if there is a snap pool on the table
  snapTime = 0 # how long there has been a snap on the table, in seconds
  snapPoolTime = 0 # how long there has been a snap pool on the table, in seconds
  pool = []
  players = [] # list of active players in the game
  draw(players,pool) # start the display
  
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
    numplayers = 4 # must be between 2 and 4
    for i in range(0,numplayers):
      players.append(Player(i))
    playerCounter = 0 # keeps track of whose turn it is
    
    # deal the cards
    random.shuffle(deck) # shuffle first
    for card in deck:
      players[playerCounter].facedown.append(card)
      playerCounter = (playerCounter+1) % numplayers
    playerCounter = 0 # need to reinitialise this
    draw(players,pool)

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
            
          elif pygame.key.get_pressed()[pygame.K_SPACE] and not players[0].knockedOut: # player has snapped!
            if checkSnap(players,0): # good snap!
              snapTime = 0 # reset the clock
              snap = False
            else: # bad snap
              pool[:] = badSnap(players[0],pool)
              snapPool = isSnapPool(players,pool)
            winner = checkWinner(players) # check for a victor
            waitCount = 0 # reset the counter
            draw(players,pool)
                
          elif pygame.key.get_pressed()[pygame.K_RETURN] and not players[0].knockedOut: # player has snap pooled!
            if checkSnapPool(players,pool,0): # good snap pool
              snapPoolTime = 0 # reset the clock
              pool[:] = [] # empty the pool
            else: # bad snap pool
              pool[:] = badSnap(players[0],pool) 
            # check again for a snap / snap pool
            snap = isSnap(players)
            snapPool = isSnapPool(players,pool)            
            winner = checkWinner(players) # check for a victor       
            waitCount = 0 # reset the counter 
            draw(players,pool)
          
      # AI here!
      # cycle through players
      for i in range(1,len(players)):
        p = players[i]
        if p.knockedOut:
          # eliminated players cannot call snap
          continue
        if snapTime > cs.AIMINCALLTIME:
          rand = random.random() 
          thresh = 1.0 - (1.0-p.CALLCHANCE)**(1.0/(cs.FPS))
          if rand < thresh or cs.INSTANTPLAY: # call snap!
            print("CPU snap at %f seconds, at roll %f against %f" % (snapTime,rand,thresh))
            if checkSnap(players,p.IND): # good snap, but this is certain
              snapTime = 0 # reset the clock
              snap = False
            winner = checkWinner(players) # check for a victor
            waitCount = 0 # reset the counter 
            draw(players,pool)
        
        if snapPoolTime > cs.AIMINCALLTIME:
          rand = random.random() 
          thresh = 1.0 - (1.0-p.CALLCHANCE)**(1.0/(cs.FPS))
          if rand < thresh or cs.INSTANTPLAY: # call snap pool!
            print("CPU snap at %f seconds, at roll %f against %f" % (snapTime,rand,thresh))
            if checkSnapPool(players,pool,p.IND): # good snap pool, but this is certain
              snapPoolTime = 0 # reset the clock
              pool[:] = [] # empty the pool
            # check again for a snap / snap pool
            snap = isSnap(players)
            snapPool = isSnapPool(players,pool)            
            winner = checkWinner(players) # check for a victor       
            waitCount = 0 # reset the counter   
            draw(players,pool)
            
      # next player takes their turn
      if waitCount >= cs.FPS*cs.TURNTIME and not winner:
      #if True: # use this for instant play
        # all this code happens once a turn!      
        waitCount = 0
        print("Player %d playing" % (playerCounter+1))
        players[playerCounter].turn() # player does their turn
        draw(players,pool)
        snap = isSnap(players)
        snapPool = isSnapPool(players,pool)
          
        # increment playerCounter
        playerCounter = (playerCounter+1) % numplayers
        while players[playerCounter].knockedOut: # cannot play if knocked out
          playerCounter = (playerCounter+1) % numplayers
        
      # increase counters
      if snap:
        snapTime = snapTime + 1.0/cs.FPS
      else:
        snapTime = 0
      if snapPool:
        snapPoolTime = snapPoolTime + 1.0/cs.FPS
      else: 
        snapPoolTime = 0
      waitCount = waitCount + 1
      clock.tick(cs.FPS) # update x times a second
      #print(clock.get_fps()) # print out the current FPS
      
    # game ended            
    print("")
    if winner > 0:
      print("Player %d wins!" % winner)
    else:
      print("No winner!")
    print("Returning to main menu")
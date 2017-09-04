# Author: George Sproston
# Created: 2017/07/12
# Updated: 2017/09/01
# Snap card game

import pygame
from pygame.locals import *
import window
import menus
import regsnap
from constants import FPS

def draw(menu):
  # should only really be drawing menus here
  screen = pygame.display.get_surface()
  screen.fill(Color(255,255,255))
  screen.blit(menu.getSurface(),getMenuPos(menu)) #combine surfaces
  #pygame.draw.rect(screen,Color(0,0,0),menu.getSurface().get_rect().move(getMenuPos(menu)),1) # draw a rectangle around the menu
  pygame.display.flip()
 
# returns top left menu position in (x,y) format
def getMenuPos(menu):
  screen = pygame.display.get_surface()
  return ((screen.get_width()-menu.w)/2.0,(screen.get_height()-menu.h)/2.0)

def forceFade(menu):
  clock = pygame.time.Clock()
  while not menu.isFaded():
    menu.fade()
    draw(menu)
    clock.tick(FPS)
  
# immediately hides and fades the given menu
def forceHide(menu):
  menu.hide()
  forceFade(menu)
    
# immediately shows and fades the given menu
def forceShow(menu):
  menu.show()
  forceFade(menu)

# called when the start button on the main menu is pressed
def startRegSnap():
  forceHide(activeMenu)
  # play snap
  regsnap.start()
  # fade menu back in
  forceShow(activeMenu)
    
# called when the exit button is pressed
def exitGame():
  global shutdown
  shutdown = True
  # fade menu out
  forceHide(activeMenu)
  
# fades out old menu, fades in the new one
def changeMenu(menu):
  global activeMenu
  forceHide(activeMenu)
  activeMenu = menu
  forceShow(activeMenu)

if __name__ == "__main__":
  print("Starting")
  pygame.init()
  window.init()
  clock = pygame.time.Clock()
  
  # init menus
  gameplayMenu = menus.initGameplayMenu()
  displayMenu = menus.initDisplayMenu()
  audioMenu = menus.initAudioMenu()
  optionsMenu =  menus.initOptionsMenu(lambda:changeMenu(gameplayMenu),lambda:changeMenu(displayMenu),lambda:changeMenu(audioMenu))
  mainMenu = menus.initMainMenu(startRegSnap,lambda:changeMenu(optionsMenu),exitGame)
  # add remaining commands now that the other menus have been initialised
  optionsMenu.addCommand("Back",lambda:changeMenu(mainMenu))
  gameplayMenu.addCommand("Back",lambda:changeMenu(optionsMenu))
  displayMenu.addCommand("Back",lambda:changeMenu(optionsMenu))
  audioMenu.addCommand("Back",lambda:changeMenu(optionsMenu))
  
  activeMenu = mainMenu
  activeMenu.show()
  menuPos = getMenuPos(activeMenu)
  
  # variables
  shutdown = False
  
  while not shutdown:  
    # show main menu
    activeMenu.fade()
    draw(activeMenu)
    
    for event in pygame.event.get(): #runs when an event occurs
      if event.type == QUIT: #quit called, exit immediately
        shutdown = True
      
      elif event.type == KEYDOWN: #key has been pressed
        if pygame.key.get_pressed()[pygame.K_ESCAPE]: # quit the game slowly
          exitGame()
      
      elif event.type == MOUSEMOTION: # mouse moved
        menuPos = getMenuPos(activeMenu)
        mpos = pygame.mouse.get_pos()
        activeMenu.movement(mpos[0]-menuPos[0],mpos[1]-menuPos[1])
      
      elif event.type == MOUSEBUTTONDOWN: #mouse clicked
        menuPos = getMenuPos(activeMenu)
        mpos = pygame.mouse.get_pos()
        if Rect(menuPos,activeMenu.getDims()).collidepoint(mpos):
          # if mouse is clicked on the menu, figure out where
          activeMenu.click(mpos[0]-menuPos[0],mpos[1]-menuPos[1])
    
    clock.tick(FPS)
  
  #regsnap.start(screen)
  
  pygame.quit()
  print("Exiting game safely")
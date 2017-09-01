from classes import Menu, Button

def initMainMenu(startcom,optcom,exitcom):
  menu = Menu("Main Menu")
  menu.addButton(Button("Start",startcom))
  menu.addButton(Button("Options",optcom))
  menu.addButton(Button("Credits",None))
  menu.addButton(Button("Exit",exitcom))
  menu.calcHeight()
  return menu
  
def initPauseMenu():
  menu = Menu("Paused")
  menu.addButton(Button("Options",None))
  menu.addButton(Button("Back",None))
  menu.addButton(Button("Main Menu",None))
  menu.calcHeight()
  return menu
  
def initOptionsMenu(gpcom,dispcom,audcom):
  menu = Menu("Options")
  menu.addButton(Button("Gameplay",gpcom))
  menu.addButton(Button("Display",dispcom))
  menu.addButton(Button("Audio",audcom))
  menu.addButton(Button("Back",None)) # added after due to dependencies
  menu.calcHeight()
  return menu
  
def initGameplayMenu():
  menu = Menu("Gameplay")
  menu.addButton(Button("Back",None)) # added after due to dependencies
  menu.calcHeight()
  return menu
  
def initDisplayMenu():
  menu = Menu("Display")
  menu.addButton(Button("Back",None)) # added after due to dependencies
  menu.calcHeight()
  return menu
  
def initAudioMenu():
  menu = Menu("Audio")
  menu.addButton(Button("Back",None)) # added after due to dependencies
  menu.calcHeight()
  return menu
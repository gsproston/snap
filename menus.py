from classes import Menu
import constants as cs # for ratios and resolutions

def res2string(ind):
  ress = []
  for resolution in cs.RESS[ind]:
    ress.append("%dx%d" % (resolution[0],resolution[1]))
  return ress

def initMainMenu(startcom,optcom,exitcom):
  menu = Menu("Main Menu")
  menu.addButton("Start",startcom)
  menu.addButton("Options",optcom)
  menu.addButton("Credits",None)
  menu.addButton("Exit",exitcom)
  menu.calcDims()
  return menu
  
def initPauseMenu():
  menu = Menu("Paused")
  menu.addButton("Options",None)
  menu.addButton("Back",None)
  menu.addButton("Main Menu",None)
  menu.calcDims()
  return menu
  
def initOptionsMenu(gpcom,dispcom,audcom):
  menu = Menu("Options")
  menu.addButton("Gameplay",gpcom)
  menu.addButton("Display",dispcom)
  menu.addButton("Audio",audcom)
  menu.addButton("Back",None) # added after due to dependencies
  menu.calcDims()
  return menu
  
def initGameplayMenu():
  menu = Menu("Gameplay")
  menu.addButton("Back",None) # added after due to dependencies
  menu.calcDims()
  return menu
  
def initDisplayMenu(opencom,closecom,ratcom):
  menu = Menu("Display")
  menu.addDropdown("Ratio",cs.RATIOS,opencom,closecom,ratcom)
  menu.addDropdown("Resolution",res2string(0),opencom,closecom,ratcom)
  menu.addButton("Back",None) # added after due to dependencies
  menu.calcDims()
  return menu
  
def initAudioMenu():
  menu = Menu("Audio")
  menu.addButton("Back",None) # added after due to dependencies
  menu.calcDims()
  return menu
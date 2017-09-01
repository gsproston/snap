from distutils.core import setup
import py2exe, os

includes = ["classes","constants","menus","regsnap","window"]
dataFiles = []
for files in os.listdir('images/'):
  f1 = 'images/' + files
  if os.path.isfile(f1): # skip directories
    f2 = 'images', [f1]
    dataFiles.append(f2)

setup(console=["main.py"],data_files=dataFiles)
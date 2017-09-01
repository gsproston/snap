from distutils.core import setup
import py2exe, os

includes = ["classes","window"]
dataFiles = []
for files in os.listdir('images/'):
  f1 = 'images/' + files
  if os.path.isfile(f1): # skip directories
    f2 = 'images', [f1]
    dataFiles.append(f2)

setup(console=["snapdisp.py"],data_files=dataFiles)
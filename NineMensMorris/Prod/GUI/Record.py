"""
file spec
action|player|startLocation|endingLocation
start location ignored for place and remove
ending location used for remove
move used for fly
"""
from datetime import datetime

class Record:
  #region Properties
  logging = " "
  fileName = ""
  #endregion  

  #region constants
  delimiter = "|"
  place = "placed"
  remove = "removed"
  move = "move"
  unused = ""
  #endregion

  #region constructor
  def __init__(self):
    logging = ""
    
    fileName = str(datetime.now())
    fileName += ".txt"
  #endregion
  
  #region methods
  def logMove(self, player, startLoc, finishLoc):
    self.logging.join([self.move,self.delimiter,str(player),self.delimiter,str(startLoc),self.delimiter,str(finishLoc),'\newline'])

  def logRemove(self,player,removedLoc):
    self.logging.join([self.remove,self.delimiter,str(player),self.delimiter,self.unused,self.delimiter,str(removedLoc),'\newline'])

  def logPlace(self,player,placedLoc):
    self.logging.join([self.place,self.delimiter,str(player),self.delimiter,self.unused,self.delimiter,str(placedLoc),'\newline'])

  def writeFile(self):
    file = open(".Log\\" + self.fileName,"w+")
    file.write(self.logging)
    file.close()


  #endregion
    





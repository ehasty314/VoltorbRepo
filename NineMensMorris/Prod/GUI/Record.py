"""
file spec
action|player|startLocation|endingLocation
start location ignored for place and remove
ending location used for remove
move used for fly
"""
import datetime

class Record(self):
  #region Properties
  logging
  fileName
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
    fileName = datetime.now() + ".txt"
  #endregion
  
  #region methods
  def logMove(self, player, startLoc, finishLoc):
    logging.append(move + delimiter + player + delimiter + startLoc + delimiter + finishLoc + '\newline')

  def logRemove(self,player,removedLoc):
    logging.append(remove + delimiter + player + delimiter + unused + delimiter + removedLoc + '\newline')

  def logPlace(self,player,placedLoc):
    logging.append(place + delimiter + player + delimiter + unused + delimiter + placedLoc + '\newline')

  def writeFile(self):
    file = open("..\\NineMensMorris\\Prod\Log\\" + fileName,"w+")
    file.write(logging)
    file.close()

print(filename)
  #endregion
    





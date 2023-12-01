"""
file spec
action|player|startLocation|endingLocation
start location ignored for place and remove
ending location used for remove
move used for fly
"""
from datetime import datetime
import os

class R:
  #region Properties
  logging = ""
  fileName = ""
  #endregion  

  #region constants
  delimiter = "|"
  place = "place"
  remove = "remove"
  move = "move"
  unused = ""
  #endregion

  #region constructor
  def __init__(self):
    logging = ""
    fileName = str(datetime.now())
    fileName += ".txt"
    self.logging = ""

  #endregion
  
  #region methods
  def logMove(self, player, startLoc, finishLoc):
    self.logging = self.logging + self.move + self.delimiter + str(player) + self.delimiter + str(startLoc) + self.delimiter + str(finishLoc) + '\n' 

  def logRemove(self,player,removedLoc):
    self.logging = self.logging + self.remove + self.delimiter + str(player) + self.delimiter + self.unused + self.delimiter + str(removedLoc) + '\n'

  def logPlace(self,player,placedLoc):
    self.logging = self.logging + self.place + self.delimiter + str(player) + self.delimiter + self.unused + self.delimiter + str(placedLoc) + '\n'

  def writeFile(self):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{current_time}.txt"

    # Adjust the path to the Log directory
    log_dir = os.path.join(".", "Log")

    # Check and create the directory if it doesn't exist
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
            print(f"Directory created: {log_dir}")
        except Exception as e:
            print(f"Error creating directory: {e}")
            return

    # Construct the full file path
    file_path = os.path.join(log_dir, file_name)

    # Attempt to write to the file
    try:
        with open(file_path, "w+") as file:
            file.write(self.logging)
        print(f"File written successfully: {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
    file.close()

  # def readFile(self):
  #endregion
    
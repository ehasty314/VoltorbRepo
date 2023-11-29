"""
file spec
action|player|startLocation|endingLocation
start location ignored for place and remove
ending location used for remove
move used for fly
"""
from datetime import datetime
import os

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
    self.logging = ""
  #endregion
  
  #region methods
  def logMove(self, player, startLoc, finishLoc):
    self.logging.join([self.move,self.delimiter,str(player),self.delimiter,str(startLoc),self.delimiter,str(finishLoc),'\newline'])

  def logRemove(self,player,removedLoc):
    self.logging.join([self.remove,self.delimiter,str(player),self.delimiter,self.unused,self.delimiter,str(removedLoc),'\newline'])

  def logPlace(self,player,placedLoc):
    self.logging.join([self.place,self.delimiter,str(player),self.delimiter,self.unused,self.delimiter,str(placedLoc),'\newline'])

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

  # def readFile(self):
  #endregion
    





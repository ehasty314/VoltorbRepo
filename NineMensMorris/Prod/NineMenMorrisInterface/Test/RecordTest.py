import unittest
from NineMensMorris.Prod.GUI.Record import Record
import os
from datetime import datetime

class TestRecord(unittest.TestCase):

    def setUp(self):
        self.log = Record()

    def test_log_Move_Successful(self):
        self.log.logMove(player=1,startLoc=0,finishLoc=1)
        self.assertEqual(" ".join([self.log.move,self.log.delimiter,str(1),self.log.delimiter,str(0),self.log.delimiter,str(1),'\newline']),self.log.logging)

    def test_writeFile_Success(self):
        self.log.logging = 'Success!'
        self.log.writeFile()
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{current_time}.txt"
        log_dir = os.path.join(".", "Log")
        file_path = os.path.join(log_dir, file_name)
        self.assertTrue(os.path.exists(log_dir))
        with open(file_path, "r") as file:
            content = file.readlines()
        for line in content:
            print(line.strip())
            self.assertEqual('Success!',line.strip())


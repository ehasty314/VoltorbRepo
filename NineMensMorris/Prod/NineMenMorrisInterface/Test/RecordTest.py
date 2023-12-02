import unittest
from Record import R
import os

class TestRecord(unittest.TestCase):
    def setUp(self):
        self.log = R()

    def test_log_move(self):
      self.log.logging = ""
      self.log.logMove(1,1,2)
      self.assertTrue(self.log.logging == "move|1|1|2\n")
      self.log.logMove(2,2,3)
      self.assertTrue(self.log.logging == "move|1|1|2\nmove|2|2|3\n")

    def test_log_place(self):
      self.log.logging = ""
      self.log.logPlace(1,1)
      self.assertTrue(self.log.logging == "place|1||1\n")
      self.log.logPlace(2,2)
      self.assertTrue(self.log.logging == "place|1||1\nplace|2||2\n")

    def test_log_remove(self):
      self.log.logging = ""
      self.log.logRemove(1,1)
      self.assertTrue(self.log.logging == "remove|1||1\n")
      self.log.logRemove(2,2)
      self.assertTrue(self.log.logging == "remove|1||1\nremove|2||2\n")

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

      #file.close()
      #if os.path.isfile(file):
      #  os.remove(file)
      
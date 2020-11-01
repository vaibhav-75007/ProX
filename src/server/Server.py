'''
This file is part of ProX.

ProX is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ProX is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ProX.  If not, see <https://www.gnu.org/licenses/>
'''

import threading
from time import sleep
from Database import DB

class Server:
    def __init__(self, db_path, idle=10):
        self.DBPath = db_path  # Path to the JSON file containing the app's database
        
        # Attributes for the idle timer
        self.TimerThread = threading.Thread(target=self.IdleTimer, daemon=True)
        self.Idle = idle
        self.Countdown = idle
        self.DBLoaded = False

        self.TimerThread.start()
    
    def LoadDB(self):
        """
        Load the database from JSON file into memory
        """
        self.DB = DB(self.DBPath)
        self.DBLoaded = True

    def UnloadDB(self):
        """
        Save the database to JSON and unload it from memory
        """
        self.DB.SaveDB()
        del self.DB
        self.DBLoaded = False

    def IdleTimer(self):
        """
        Decrease Countdown attribute every second
        """
        while True:
            if self.DBLoaded and self.Countdown > 0:
                sleep(1)
                self.Countdown -= 1
            elif self.Countdown == 0:
                self.UnloadDB()
                self.Countdown = self.Idle

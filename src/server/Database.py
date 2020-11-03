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

import json
from time import time

class DB:
    def __init__(self, db_path):
        self.DBPath = db_path
        
        with open(db_path, 'r') as db:
            self.Users = json.load(db)

        self.Ids = dict()  # Dictionary of position of each user's ID in the Users list. Optimized for O(1) query time
        for idx, user in enumerate(self.Users):
            self.Ids[user["id"]] = idx

    def SaveDB(self):
        with open(self.DBPath, 'w') as db:
            json.dump(self.Users, db)

    def FindUserByEmail(self, email) -> dict:
        """
        Search for the user with the provided email then return the corresponded user object, or None if not found
        """
        for user in self.Users:
            if user["email"] == email:
                return user
        return None

    def AddUser(self, name, email, pin) -> dict:
        """
        Add a brand new user with blank data then return this new user object
        """
        if len(self.Users) == 0:
            granted_id = 1
        else:
            granted_id = max(self.Users, key=lambda user: user["id"])["id"] + 1

        now = int(time())
        user = dict(
            id = granted_id,
            name = name,
            email = email,
            pin = pin,
            productivity_score = 0,
            task_completion_rate = 0,
            missed_deadline = 0,
            weekly_productivity_score = 0,
            weekly_task_completion_rate = 0,
            weekly_deadlines_missed = 0,
            tasks = list(),
            flashcards = list(),
            curriculums = list(),
            last_get = now,
            last_put = now
        )
        self.Users.append(user)
        self.Ids[granted_id] = len(self.Users) - 1
        return user

    def ModUser(self, user_id, name, email, pin, productivity_score, task_completion_rate, missed_deadline, 
                weekly_productivity_score, weekly_task_completion_rate, weekly_deadlines_missed,
                tasks, flashcards, curriculums):
        """
        Modify an existing user then return this user object
        """
        now = int(time())
        self.Users[self.Ids[user_id]] = dict(
            id = user_id,
            name = name,
            email = email,
            pin = pin,
            productivity_score = productivity_score,
            task_completion_rate = task_completion_rate,
            missed_deadline = missed_deadline,
            weekly_productivity_score = weekly_productivity_score,
            weekly_task_completion_rate = weekly_task_completion_rate,
            weekly_deadlines_missed = weekly_deadlines_missed,
            tasks = tasks,
            flashcards = flashcards,
            curriculums = curriculums,
            last_get = now,
            last_put = now
        )
        user = self.Users[self.Ids[user_id]]
        return user

    def DelUser(self, user_id):
        """
        Delete a user entirely
        """
        del self.Users[self.Ids[user_id]]
        del self.Ids[user_id]

    def QueryUser(self, user_id) -> dict:
        """
        Return the queried user object
        """
        if user_id not in self.Ids:
            raise KeyError(f"User ID #{user_id} not found")
        user = self.Users[self.Ids[user_id]]
        now = int(time())
        user["last_get"] = now
        return user

    @staticmethod
    def TypeCheckNewUser(data):
        """
        Check and validate the input data for creating a new user.
        Raise exception if any errors found.
        """
        user_types = dict(
            name = str,
            email = str,
            pin = int
        )
        for attr in data:
            if type(data[attr]) != user_types[attr]:
                raise TypeError(f"Type error {attr} in user data. Expected {user_types[attr]}. Found {type(data[attr])}")
    
    @staticmethod
    def TypeCheckExistingUser(data):
        """
        Check and validate the input data for existing user to match DB's correct data types.
        Raise exception if any errors found.
        """
        from datetime import datetime

        user_types = dict(
            id = int,
            name = str,
            email = str,
            pin = int,
            productivity_score = int,
            task_completion_rate = int,
            missed_deadline = int,
            weekly_productivity_score = int,
            weekly_task_completion_rate = int,
            weekly_deadlines_missed = int,
            tasks = list,
            flashcards = list,
            curriculums = list,
            last_get = int,
            last_put = int
        )
        task_types = dict(
            name = str,
            description = str,
            deadline = str
        )
        flashcard_types = dict(
            subject = str,
            front_text = str,
            back_text = str
        )
        curriculum_types = dict(
            name = str,
            subject = str,
            topics = list
        )

        for attr in data:
            if type(data[attr]) != user_types[attr]:
                raise TypeError(f"Type error {attr} in user data. Expected {user_types[attr]}. Found {type(data[attr])}")

        for task in data["tasks"]:
            if type(task) != dict:
                raise TypeError(f"{task} is not type dict")
            for attr in task:
                if type(task[attr]) != task_types[attr]:
                    raise TypeError(f"Type error {attr} in {task}. Expected {task_types[attr]}. Found {type(task[attr])}")
            try:
                datetime.strptime(task["deadline"], '%Y/%m/%d %H:%M:%S')
            except:
                raise Exception(f"String formatted time not correct in {task}. Must be YYYY/mm/dd HH:MM:SS")

        for flashcard in data["flashcards"]:
            if type(flashcard) != dict:
                raise TypeError(f"{flashcard} is not type dict")
            for attr in flashcard:
                if type(flashcard[attr]) != flashcard_types[attr]:
                    raise TypeError(f"Type error {attr} in {flashcard}. Expected {flashcard_types[attr]}. Found {type(flashcard[attr])}")

        for curriculum in data["curriculums"]:
            if type(curriculum) != dict:
                raise TypeError(f"{curriculum} is not type dict")
            for attr in curriculum:
                if type(curriculum[attr]) != curriculum_types[attr]:
                    raise TypeError(f"Type error {attr} in {curriculum}. Expected {curriculum_types[attr]}. Found {type(curriculum[attr])}")
            for topic in curriculum["topics"]:
                if type(topic) != str:
                    raise TypeError(f"{topic} is not type str")

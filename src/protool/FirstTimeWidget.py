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

# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog,QDialogButtonBox,QLineEdit,QFormLayout,QHBoxLayout,QVBoxLayout,QLabel,QDialog
import json
import requests
import user_class as user
import flashcard_class as flash
import Task as task
import curriculum
import jsonUtil as js
import sys
import datetime

#work on case for null tasks, curriculums and flashcards list
#work on requests for modifying user and deleting a user
#work on curriculums widget and making gui better

class FirstTimeWindow(QDialog):
    def __init__(self,*args,**kwargs):
        super(FirstTimeWindow,self).__init__(*args,**kwargs)

        self.layout = QVBoxLayout()
        self.form = QHBoxLayout()
        self.description = QHBoxLayout()
        self.description.addWidget(QLabel("Login"))
        self.description.addWidget(QLabel("Sign Up"))

        self.loginForm = QFormLayout()
        self.signupForm = QFormLayout()

        self.signupUsername = QLineEdit()
        self.signupEmail = QLineEdit()
        self.signupPasswords = [QLineEdit(),QLineEdit()]

        self.loginUsername = QLineEdit()
        self.loginPassword = QLineEdit()

        self.loginForm.addRow(QLabel("Email:"),self.loginUsername)
        self.loginForm.addRow(QLabel("Pin:"),self.loginPassword)

        self.signupForm.addRow(QLabel("Username:"),self.signupUsername)
        self.signupForm.addRow(QLabel("Email:"),self.signupEmail)
        self.signupForm.addRow(QLabel("Pin:"),self.signupPasswords[0])
        self.signupForm.addRow(QLabel("Confirm Pin"),self.signupPasswords[1])
        self.form.addLayout(self.loginForm)
        self.form.addLayout(self.signupForm)

        self.layout.addLayout(self.description)
        self.layout.addLayout(self.form)

        self.button = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button.accepted.connect(self.checkCredentials)
        self.button.rejected.connect(sys.exit)

        self.layout.addWidget(self.button)
        self.setWindowTitle("Login/Sign up")

        self.setLayout(self.layout)

    def checkCredentials(self): #validate data
        while True:
            try:
                if self.signupUsername.text() != "" and self.signupPasswords[0].text() != "" and self.signupPasswords[1].text() != "" and self.signupEmail.text() != "" and isinstance(int(self.signupPasswords[0].text()),int):
                    self.signup()
                    break
                elif self.loginUsername.text() != "" and self.loginPassword != "" and isinstance(int(self.loginPassword.text()),int): #make sure the pin entered is an int
                    self.login()
                    break
            except TypeError:
                dialog = QDialog()
                dialog.setWindowTitle("Pin must be a number")
                dialog.setText("Your pin must be a number!")
                dialog.exec_()

    def signup(self): #for creating new account
        if self.signupPasswords[0].text() != self.signupPasswords[1].text():
            return

        self.pin = int(self.signupPasswords[0].text())

        data = {"name":str(self.signupUsername.text()),"email":str(self.signupEmail.text()),"pin":self.pin}

        r = requests.post('http://0.0.0.0:54321/new/',json=data)
        print(r.status_code)
        newUser = r.json()

        user.user = user.User(idNo=newUser["id"],name=newUser["name"],email=newUser["email"],pin=newUser["pin"],deadlines_missed=0,task_completion_rate=0,productivity_score=0,week_task_completion_rate=0,week_productivity_score=0,week_deadline_missed=0)
        flash.flashcards = []
        task.tasks = []
        curriculum.curriculums = []

        with open("data.json",'wt') as file:
            string = user.user.__dict__()
            string["tasks"] = []
            string["flashcards"] = []
            string["curriculums"] = []
            file.write(json.dumps(string))

        js.writeDateLastOn()
        self.hide()

    def login(self): #for recovering from an existing account
        data = {"pin":int(self.loginPassword.text()),"email":self.loginUsername.text()}
        r = requests.get('http://0.0.0.0:54321/recover/',json=data)
        print(r.status_code)
        recoveredUser = r.json()
        user.user = user.User(idNo=recoveredUser["id"],name=recoveredUser["name"],email=recoveredUser["email"],pin=recoveredUser["pin"],task_completion_rate=recoveredUser["task_completion_rate"],deadlines_missed=recoveredUser["missed_deadline"],productivity_score=0,week_productivity_score=recoveredUser["weekly_productivity_score"],week_deadline_missed=recoveredUser["weekly_deadlines_missed"],week_task_completion_rate=recoveredUser["weekly_task_completion_rate"])
        task.tasks = [task.Task(name=tempDict["name"],deadline=js.stringToDatetime(tempDict["deadline"]),description=tempDict["description"]) for tempDict in recoveredUser["tasks"]]
        flash.flashcards = [flash.FlashCard(subject=tempDict["subject"],front_text=tempDict["front_text"],back_text=tempDict["back_text"]) for tempDict in recoveredUser["flashcards"]]
        curriculum.curriculums = [curriculum.Curriculum(name=tempDict["name"],subject=tempDict["subject"],topics=tempDict["topics"]) for tempDict in recoveredUser["curriculums"]]

        js.writeAll(user.user,curriculum.curriculums,task.tasks,flash.flashcards)

        self.close()

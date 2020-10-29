# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog,QDialogButtonBox,QLineEdit,QFormLayout,QHBoxLayout,QVBoxLayout
import json
import requests
import user_class as user
import flashcard_class as flash
import Task as task
import curriculum
import jsonUtil as js


class FirstTimeWindow(QDialog):
    def __init__(self,*args,**kwargs):
        super(FirstTimeWidget,self).__init__(*args,**kwargs)

        self.layout = QHBoxLayout()
        self.form = QVBoxLayout()

        self.loginForm = QFormLayout()
        self.signupForm = QFormLayout()

        self.signupUsername = QLineEdit()
        self.signupEmail = QLineEdit()
        self.signupPasswords = [QLineEdit(),QLineEdit()]

        self.loginUsername = QLineEdit()
        self.loginPassword = QLineEdit()

        self.loginForm.addRow(QLabel("Email:"),loginUsername)
        self.loginForm.addRow(QLabel("Password:"),loginPassword)

        self.signupForm.addRow(QLabel("Username:"),signupUsername)
        self.signupForm.addRow(QLabel("Email:"),signupEmail)
        self.signupForm.addRow(QLabel("Password:"),signupPasswords[0])
        self.signupForm.addRow(QLabel("Confirm Password"),signupPasswords[1])
        self.form.addLayout(self.loginForm)
        self.form.addLayout(self.signupForm)

        self.layout.addLayout(self.form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button.accepted.connect(self.checkCredentials)
        self.button.rejected.connect(sys.exit)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def checkCredentials(self):
        while True:
            if self.signupUsername.text() != "" and self.signupPasswords[0].text() != "" and self.signupPasswords[1].text() != "" and self.signupEmail.text() != "":
                self.signup()
                break
            elif self.loginUsername.text() != "" and self.loginPassword != "":
                self.login()
                break

    def signup(self):
        if self.signupPasswords[0] != self.signupPasswords[1]:
            return
        data = {"name":self.signupUsername.text(),"email":self.signupEmail.text(),"pin":self.signupPasswords[0].text()}
        r = requests.post('http://localhost.5000/new/',json=data)
        newUser = r.data
        user.user = user.User(idNo=newUser["id"],name=newUser["name"],email=newUser["email"],password=newUser["pin"],deadlines_missed=0,task_completion_rate=0,productivity_score=0,week_task_completion_rate=0,week_productivity_score=0,week_deadline_missed-0)
        flash.flashcards = []
        task.tasks = []

        with open("data.json",'wt') as file:
            string = dict(user.user)
            string["tassk"] = []
            string["flashcards"] = []
            string["curriculums"] = []
            file.write(json.dumps(string))

        self.close()

    def login(self):
        data = {"pin":self.loginPassword.text(),"email":self.loginUsername.text()}
        r = requests.get('http://localhost.5000/recover/',json=data)
        recoveredUser = r.data
        user.user = user.User(idNo=recoveredUser["id"],name=recoveredUser["name"],email=recoveredUser["email"],password=recoveredUser["pin"],task_completion_rate=recoveredUser["task_completion_rate"],deadlines_missed=recoveredUser["deadlines_missed"],productivity_score=recoveredUser["productivity_score"],week_productivity_score=recoveredUser["week_productivity_score"],week_deadline_missed=recoveredUser["week_deadline_missed"],week_task_completion_rate=recoveredUser["week_task_completion_rate"])
        task.tasks = [task.Task(name=tempDict["name"],deadline=js.stringToDatetime(tempDict["deadline"]),description=tempDict["description"]) for tempDict in recoveredUser["tasks"]]
        flash.flashcards = [flash.FlashCard(subject=tempDict["subject"],front_text=tempDict["front_text"],back_text=tempDict["back_text"]) for tempDict in recoveredUser["flashcards"]]
        curriculum.curriculums = [curriculum.Curriculum(name=tempDict["name"],subject=tempDict["subject"],topics=tempDict("topics")) for tempDict in recoveredUser["curriculums"]]

        js.writeAll()

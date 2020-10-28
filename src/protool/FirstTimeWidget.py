# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog,QDialogButtonBox,QLineEdit,QFormLayout,QHBoxLayout,QVBoxLayout
import json


class FirstTimeWindow(QDialog):
    def __init__(self,*args,**kwargs):
        super(FirstTimeWidget,self).__init__(*args,**kwargs)

        self.layout = QHBoxLayout()
        self.form = QVBoxLayout()

        self.loginForm = QFormLayout()
        self.signupForm = QFormLayout()

        self.signupUsername = QLineEdit()
        self.signupPasswords = [QLineEdit(),QLineEdit()]

        self.loginUsername = QLineEdit()
        self.loginPassword = QLineEdit()

        self.loginForm.addRow(QLabel("Username:"),loginUsername)
        self.loginForm.addRow(QLabel("Password:"),loginPassword)

        self.signupForm.addRow(QLabel("Username:"),signupUsername)
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
            if self.signupUsername.text() != "" and self.signupPasswords[0].text() != "" and self.signupPasswords[1].text() != "":
                self.signup()
                break
            elif self.loginUsername.text() != "" and self.loginPassword != "":
                self.login()
                break

    def signup(self):
        with open("data.json",'wt') as file:
            #get valid user id from database
            file.write()

    def login(self):
        pass

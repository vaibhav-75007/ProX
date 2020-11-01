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
from PySide2.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout, QDialogButtonBox


class InfoDialog(QDialog):
    def __init__(self,*args,**kwargs):
        super(InfoDialog,self).__init__(*args,**kwargs)
        #initialise the parent QDialog
        self.text = QPlainTextEdit(self) #create a text edit to show the about section
        self.text.setPlainText("About this app: a productivity tool with pomodoro timer, todo list, leaderboard and more to make productivity competitive\nCreated by:\nvision-05\nMartian\ndemigod\ndqtvictory\nalfred")

        self.dialog = QDialogButtonBox(QDialogButtonBox.Ok)
        self.dialog.accepted.connect(self.close) #create a button to close the dialog

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.dialog)
        self.setLayout(self.layout) #set everythin in a vertical layout

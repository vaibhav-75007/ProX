# This Python file uses the following encoding: utf-8
import sys
import os
import InfoDialog
import flashcard_class as flash
import user_class as user
import curriculum
import Task as task
from datetime import datetime
import FirstTimeWidget as first
import jsonUtil as js
import requests
import copy

from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QGridLayout, QPushButton, QWidget, QSpacerItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QBrush, QColor, QPalette

"""
Create dialog to create flashcards, delete flashcards
Create separate dialog to create a new set of flashcards or delete a set of flashcards
Create a widget to show curriculums
Create dialog to create curriculums
Create dialog to remove curriculums
Alter colors of gui elements
Use icons for buttons
Create installer application
Write data into json
Send data to db
"""


qss = """
QScrollBar {
    background-color: #AAAAAA;
    color: #ABABAB;
}

QMainWindow {
    background-color: #555555;
}

QLineEdit {
    background-color: #ABABAB;
    color: white;
}

QSpinBox {
    background-color: #ABABAB;
    color: white;
}

QDialog {
    background-color: #555555;
}

QPushButton {
    background-color: #ABABAB;
    color: white;
}

QPlainTextEdit {
    background-color: #555555;
    color: white;
}

QMenuBar {
    color: white;
    background-color: gray;
}

QMenuBar::item::selected {
    background-color: #ABABAB;
}

QMenu {
    background-color: gray;
}

QMenu::item {
    background-color: gray;
    color: white;
}

QMenu::item::selected {
    background-color: #ABABAB;
}
QListWidget {
    background-color: #777777;
}

QListWidget::item::selected {
    background-color: #993399;
}

QStackedWidget {
    background-color: gray;
}

QLabel {
    color: white;
}
"""

def ping():
    r = requests.get('http://0.0.0.0:54321/')
    print(r.status_code)

def testOnline():
    try:
        for i in range(5):
            ping()
        return True
    except requests.exceptions.ConnectionError:
        print("could not connect to server")
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        if os.path.exists("data.json") == False:
            if testOnline() == False:
                sys.exit()

            loginWindow = first.FirstTimeWindow()
            loginWindow.exec_()

        #cases for if file is empty or invalid data

        js.readAll()

        self.load_ui()
        self.setFixedSize(1200,800)
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        self.spacer = QSpacerItem(100,100)
        self.spacer1 = QSpacerItem(100,100)

        self.layout = QGridLayout(self.centralWidget)
        self.appended = False

        if testOnline() == False:
            self.users = [user.user]
        else:
            try:
                r = requests.get('http://0.0.0.0:54321/' + str(user.user.id) + '/' + str(user.user.pin) + '/everyone/')
                self.users = [user.User(dictionary["name"],0,dictionary["task_completion_rate"],dictionary["missed_deadline"],dictionary["weekly_productivity_score"],dictionary["weekly_task_completion_rate"],dictionary["weekly_deadlines_missed"],0,0,0) for dictionary in r.json()]
                print([user.name for user in self.users])
            except TypeError:
                print("Your user account is not on the database")
                self.users = [user.user]

        self.leaderboard = user.LeaderBoard(self.users,self)
        self.layout.addWidget(self.leaderboard,0,0,1,2)

        self.layout.addItem(self.spacer,0,2,1,1)

        self.tasks = task.tasks
        self.todo = task.ToDoList(self.tasks)
        self.layout.addWidget(self.todo,0,3,1,1)

        self.layout.addItem(self.spacer1,0,4,1,1)

        self.taskInputField = task.TaskInputFieldWidget()
        self.layout.addWidget(self.taskInputField,1,3,1,1)

        self.setLayout(self.layout)
        self.menu = self.menuBar()
        self.initMenu()

        self.taskInputField.add.connect(self.todo.addTask)
        self.taskInputField.done.released.connect(self.taskInputField.createTask)

        self.flashcards = flash.flashcards

        self.setWindowTitle("ProX")

    def initMenu(self): #set up the menu bar, with File, syllabi and leaderboard
        self.filemenu = self.menu.addMenu("&File")
        self.syllabimenu = self.menu.addMenu("&Syllabi")
        self.leaderboardmenu = self.menu.addMenu("&Leader Board")
        self.flashcardmenu = self.menu.addMenu("&Flashcards")

        self.about = QAction("About App",self) #get info about the app
        self.exit = QAction("Exit",self) #exit the app
        self.delete = QAction("Delete Account",self)
        self.view = QAction("View Syllabi",self) #view the syllabi window
        self.hideSyllabi = QAction("Hide Syllabi",self) #hide the syllabi widget
        self.showSyllabi = QAction("Show Syllabi",self) #show the syllabi widget
        self.openFlashcards = QAction("View Flashcards",self)

        self.about.triggered.connect(self.info)
        self.exit.triggered.connect(sys.exit)
        self.view.triggered.connect(self.openSyllabiWindow)
        self.hideSyllabi.triggered.connect(self.hideSyllabiWidget)
        self.showSyllabi.triggered.connect(self.showSyllabiWidget)
        self.openFlashcards.triggered.connect(self.showFlashcards)
        self.delete.triggered.connect(self.deleteAccount)

        self.filemenu.addAction(self.about)
        self.filemenu.addAction(self.exit)
        self.syllabimenu.addAction(self.view)
        self.syllabimenu.addAction(self.hideSyllabi)
        self.syllabimenu.addAction(self.showSyllabi)
        self.flashcardmenu.addAction(self.openFlashcards)

    def deleteAccount(self):
        r = requests.delete('http://0.0.0.0:54321/' + str(user.user.id) + '/' + str(user.user.pin) + '/')
        os.remove("data.json")
        sys.exit()

    def showFlashcards(self):
        self.makeFlashCardWindows(self.flashcards)

    def inputFlashcardInfo(self):
        self.creator = flash.FlashCardCreateWindow()
        self.creator.show()
        self.creator.done.released.connect(self.makeNewFlashcard)

    def makeNewFlashcard(self):
        if self.creator.subjectInput.text() == "" or self.creator.frontInput.text() == "" or self.creator.backInput.text() == "":
            return

        self.flashcards.append(flash.FlashCard(self.creator.subjectInput.text(),self.creator.frontInput.text(),self.creator.backInput.text()))
        flash.flashcards = self.flashcards
        js.writeAll(user.user,curriculum.curriculums,task.tasks,flash.flashcards)

        for flashcardWindow in self.flashcardWindows:
            flashcardWindow.create.triggered.disconnect(self.inputFlashcardInfo)
            flashcardWindow.delete.triggered.disconnect(self.deleteFlashcard)

        self.creator.subjectInput.clear()
        self.creator.frontInput.clear()
        self.creator.backInput.clear()

        self.flashcardWindows.clear()
        self.makeFlashCardWindows(self.flashcards)

    def deleteFlashcard(self):
        self.deleter = flash.FlashCardDeleteWindow()
        self.deleter.show()
        self.deleter.buttonConfirm.released.connect(self.removeFlashcard)

    def removeFlashcard(self):
        self.flashcards.remove(self.deleter.index)
        js.writeAll(user.user,curriculum.curriculums,task.tasks,flash.flashcards)

    def makeFlashCardWindows(self,flashcards):
        self.flashcardWindows = []
        if flash.flashcards[0] == None:
            inputFlashcardInfo()

        flashcardsNew = flash.sortFlashcards(flashcards)
        for section in range(len(flashcardsNew)):
            self.flashcardWindows.append(flash.FlashCardWindow(flashcardsNew,section))

        for flashcardWindow in self.flashcardWindows:
            flashcardWindow.create.triggered.connect(self.inputFlashcardInfo)
            flashcardWindow.delete.triggered.connect(self.deleteFlashcard)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def info(*args): #creates a new dialog window to show the about app section
        info = InfoDialog.InfoDialog()
        info.setWindowTitle("About")
        info.exec_() #execute that window

    def openSyllabiWindow(self):
        foo = 2

    def hideSyllabiWidget(self):
        foo = 2

    def showSyllabiWidget(self):
        foo = 2

    def deleteUser(self):
        with open("data.json",'wt') as filee:
            file.write("")
        #call delete user on database


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qss)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

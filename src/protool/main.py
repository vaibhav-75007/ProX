# This Python file uses the following encoding: utf-8
import sys
import os
import InfoDialog
import flashcard_class as flash
import user_class as user
import Task as task
from datetime import datetime


from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QGridLayout, QPushButton, QWidget, QSpacerItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QBrush, QColor, QPalette

qss = """
QMenuBar {
    color: white;
    background-color: gray;
}

QMenuBar::item::selected {
    background-color: #AAAAAA;
}

QMenu {
    background-color: #ABABAB;
}

QMenu::item {
    background-color: #AAAAAA;
    color: white;
}

QMenu::item:selected {
    background-color: #AAAAAA;
}

QListWidget {
    background-color: #777777;
}

QListWidget::item::selected {
    background-color: #993399;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()
        self.setFixedSize(1200,700)
        self.centralWidget = QWidget()

        self.centralWidget.setBackgroundRole(QPalette.Window)

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window,QBrush(QColor.fromRgbF(0.3,0.3,0.3,1)))
        self.palette.setBrush(QPalette.Text,QBrush(QColor.fromRgbF(0.9,0.9,0.9,1)))

        self.centralWidget.setPalette(self.palette)
        self.centralWidget.setAutoFillBackground(True)

        self.setCentralWidget(self.centralWidget)

        self.spacer = QSpacerItem(100,100)
        self.spacer1 = QSpacerItem(100,100)

        self.layout = QGridLayout(self.centralWidget)

        self.users = [user.User("Test",4,3,4,5,4,3),user.User("Test1",3,6,43,5,3,3),user.User("Test2",3,2,5,4,3,5),user.User("Test3",3,2,5,4,3,5),user.User("Test4",3,2,5,4,3,5),user.User("Test5",3,2,5,4,3,5)]
        self.leaderboard = user.LeaderBoard(self.users,self)
        self.layout.addWidget(self.leaderboard,0,0,1,2)

        self.layout.addItem(self.spacer,0,2,1,1)

        self.tasks = [task.Task(datetime.now(),"test","test"),task.Task(datetime.now(),"test1","test1"),task.Task(datetime.now(),"test2","test2"),task.Task(datetime.now(),"test3","test3"),task.Task(datetime(2020,12,3),"test4","test4")]
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

    def initMenu(self): #set up the menu bar, with File, syllabi and leaderboard
        self.filemenu = self.menu.addMenu("&File")
        self.syllabimenu = self.menu.addMenu("&Syllabi")
        self.leaderboardmenu = self.menu.addMenu("&Leader Board")

        self.about = QAction("About App", self) #get info about the app
        self.exit = QAction("Exit", self) #exit the app
        self.view = QAction("View Syllabi", self) #view the syllabi window
        self.hideSyllabi = QAction("Hide Syllabi", self) #hide the syllabi widget
        self.showSyllabi = QAction("Show Syllabi", self) #show the syllabi widget

        self.about.triggered.connect(self.info)
        self.exit.triggered.connect(sys.exit)
        self.view.triggered.connect(self.openSyllabiWindow)
        self.hideSyllabi.triggered.connect(self.hideSyllabiWidget)
        self.showSyllabi.triggered.connect(self.showSyllabiWidget)

        self.filemenu.addAction(self.about)
        self.filemenu.addAction(self.exit)
        self.syllabimenu.addAction(self.view)
        self.syllabimenu.addAction(self.hideSyllabi)
        self.syllabimenu.addAction(self.showSyllabi)

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


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qss)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

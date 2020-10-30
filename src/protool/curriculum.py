# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QMainWindow,QLineEdit,QFormLayout,QDialogButtonBox,QWidget,QListWidget,QListWidgetItem,QStackedWidget,QMenu,QAction,QVBoxLayout,QPushButton,QLabel,QHBoxLayout
import jsonUtil as js
import user_class as user
import Task as task
import flashcard_class as flash

class Curriculum:
    def __init__(self,name,subject,topics):
        self.name = name
        self.subject = subject
        self.topics = topics

    def __dict__(self):
        return {
            "name":self.name,
            "subject":self.subject,
            "topics":self.topics
        }

class CurriculumCreateWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(CurriculumCreateWindow,self).__init__(*args,**kwargs)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.form = QFormLayout()
        self.nameInput = QLineEdit()
        self.subjectInput = QLineEdit()
        self.topicsInput = [QLineEdit()]
        self.topicsInput[0].textChanged.connect(self.addInput)
        self.currentConnected = 0
        self.done = QPushButton("Done")

        self.form.addRow(QLabel("Name:"),self.nameInput)
        self.form.addRow(QLabel("Subject:"),self.subjectInput)
        self.form.addRow(QLabel("Topics:"),self.topicsInput[0])

        self.layout.addLayout(self.form)
        self.layout.addWidget(self.done)
        self.setLayout(self.layout)

        self.setWindowTitle("Create Curriculum")

    def addInput(self):
        self.topicsInput.append(QLineEdit())
        self.topicsInput[self.currentConnected].textChanged.disconnect(self.addInput)
        self.currentConnected += 1
        self.topicsInput[self.currentConnected].textChanged.connect(self.addInput)

        self.form.addRow(QLabel(""),self.topicsInput[-1])

class CurriculumDeleteWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(CurriculumDeleteWindow,self).__init__(*args,**kwargs)
        self.curriculums = curriculums

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.buttons = QHBoxLayout()

        self.next = QPushButton("Next")
        self.confirm = QPushButton("Confirm")
        self.previous = QPushButton("Previous")

        self.buttons.addWidget(self.previous)
        self.buttons.addWidget(self.confirm)
        self.buttons.addWidget(self.next)

        self.next.released.connect(self.nextCurriculum)
        self.previous.released.connect(self.previousCurriculum)

        self.subject = QLabel(self.curriculums[0].subject)
        self.name = QLabel(self.curriculums[0].name)

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.subject)
        self.layout.addLayout(self.buttons)

        self.setLayout(self.layout)

        self.index = 0

        self.setWindowTitle("Delete Curriculum")

    def nextCurriculum(self):
        if self.index < len(self.curriculums) - 1:
            self.index += 1
        else:
            self.index = 0
        self.showCurriculum()

    def previousCurriculum(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = len(self.curriculums) - 1
        self.showCurriculum()

    def showCurriculum(self):
        self.name.setText(self.curriculums[self.index].name)
        self.subject.setText(self.curriculums[self.index].subject)

class CurriculumWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(CurriculumWindow,self).__init__(*args,**kwargs)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.curriculums = curriculums

        self.layout = QVBoxLayout(self.centralWidget)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.buttons = QHBoxLayout()
        self.next = QPushButton("Next")
        self.previous = QPushButton("Previous")
        self.buttons.addWidget(self.previous)
        self.buttons.addWidget(self.next)

        self.next.released.connect(self.nextCurriculum)
        self.previous.released.connect(self.previousCurriculum)

        self.layout.addLayout(self.buttons)
        self.index = 0

        if len(curriculums) == 0:
            self.addCurriculumCreator()
            self.hide()
        if len(curriculums) == 0:
            self.close()

        for curriculum in self.curriculums:
            self.stack.addWidget(CurriculumWidget(curriculum))

        self.setWindowTitle("Curriculums")

        self.initMenu()
        self.setLayout(self.layout)

        self.stack.setCurrentIndex(self.index)

    def nextCurriculum(self):
        if self.stack.currentIndex() < self.stack.count() - 1:
            self.index += 1
        else:
            self.index = 0
        self.stack.setCurrentIndex(self.index)

    def previousCurriculum(self):
        if self.stack.currentIndex() > 0:
            self.index -= 1
        else:
            self.index = self.stack.count() - 1
        self.stack.setCurrentIndex(self.index)

    def initMenu(self):
        self.menu = self.menuBar()
        self.file = self.menu.addMenu("&File")
        self.create = QAction("Create")
        self.delete = QAction("Delete")

        self.file.addAction(self.create)
        self.file.addAction(self.delete)

        self.create.triggered.connect(self.addCurriculumCreator)
        self.delete.triggered.connect(self.addCurriculumDeleter)

        self.setFixedSize(400,300)

    def addCurriculumCreator(self):
        self.creator = CurriculumCreateWindow()
        self.creator.show()
        self.creator.done.released.connect(self.addCurriculum)

    def addCurriculumDeleter(self):
        if len(curriculums) == 0:
            self.close()
        self.deleter = CurriculumDeleteWindow()
        self.deleter.show()
        self.deleter.confirm.released.connect(self.deleteCurriculum)

    def deleteCurriculum(self):
        curriculums.pop(self.deleter.index)
        self.stack.removeWidget(self.stack.widget(self.deleter.index))
        js.writeAll(user.user,curriculums,task.tasks,flash.flashcards)
        self.deleter.close()
        if self.stack.count() > 0:
            self.stack.setCurrentIndex(0)
        else:
            self.close()

    def addCurriculum(self):
        if self.creator.nameInput.text() == "" or self.creator.subjectInput.text() == "":
            return
        topics = [self.creator.topicsInput[i].text() for i in range(len(self.creator.topicsInput)) if self.creator.topicsInput[i].text() != ""]
        self.curriculums.append(Curriculum(self.creator.nameInput.text(),self.creator.subjectInput.text(),topics))
        print(self.curriculums[-1])
        self.stack.addWidget(CurriculumWidget(self.curriculums[-1]))

        self.creator.nameInput.clear()
        self.creator.subjectInput.clear()
        self.creator.topicsInput[-1].textChanged.disconnect(self.creator.addInput)

        self.creator.topicsInput = [QLineEdit()]

        js.writeAll(user.user,curriculums,task.tasks,flash.flashcards)
        if self.stack.count() > 0:
            self.stack.setCurrentIndex(0)
        else:
            self.close()

        self.creator.hide()
        self.creator.show()

class CurriculumWidget(QWidget):
    def __init__(self,curriculum,*args,**kwargs):
        super(CurriculumWidget,self).__init__(*args,**kwargs)

        self.curriculum = curriculum
        self.name = QLabel(self.curriculum.name)
        self.subject = QLabel(self.curriculum.subject)
        self.topics = QListWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.subject)
        self.layout.addWidget(self.topics)

        for topic in self.curriculum.topics:
            self.topics.addItem(TopicListWidgetItem(topic))

        self.setLayout(self.layout)
        self.show()

class TopicListWidgetItem(QListWidgetItem):
    def __init__(self,name,*args,**kwargs):
        super(TopicListWidgetItem,self).__init__(*args,**kwargs)

        self.setText(name)

curriculums = 0

from PySide2.QtWidgets import QStackedWidget, QLabel, QPushButton, QGridLayout, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QGridLayout, QMenu, QAction
from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtCore import Qt, Signal, Slot
import copy

class FlashCard():
    def __init__(self, subject, front_text,back_text,idNo):
        self.id = idNo
        self.subject = subject
        self.front_text = front_text
        self.back_text = back_text

    def __dict__(self):
        return {
                "id":self.idNo,
                "subject":self.subject,
                "frontText":self.front_text,
                "backText":self.back_text
               }

    def change_subject(self, text):
        self.subject = text

    def change_front_text(self,text):
        self.front_text = text
    
    def change_back_text(self,text):
        self.back_text = text

class FlashCardWidget(QWidget):
    def __init__(self,flashcard,*args,**kwargs):
        super(FlashCardWidget,self).__init__(*args,**kwargs)

        self.grid = QGridLayout()

        self.flashcard = flashcard
        self.flipped = False

        self.label = QLabel(self)
        self.label.setText(self.flashcard.front_text)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label,Qt.AlignCenter)
        self.setLayout(self.layout)
        self.label.setAlignment(Qt.AlignCenter)

        self.label.show()

        self.show()

    def flip(self):
        if self.flipped == False:
            self.label.setText(self.flashcard.back_text)
            self.flipped = True
            return
        self.label.setText(self.flashcard.front_text)
        self.flipped = False

def sortFlashcards(flashcards):
    subjects = []
    for flashcard in flashcards:
        if flashcard.subject not in subjects:
            subjects.append(flashcard.subject)

            flashcardsNew = copy.deepcopy(subjects)

    temp = []
    for i in range(len(subjects)):
        temp = []
        for flashcard in flashcards:
            if flashcard.subject == subjects[i]:
                temp.append(flashcard)

        flashcardsNew[i] = temp

    return flashcardsNew

class FlashCardWindow(QMainWindow):
    def __init__(self,flashcards,index,*args,**kwargs):
        super(FlashCardWindow,self).__init__(*args,**kwargs)

        self.flashcards = flashcards

        self.index = 0
        self.maxIndex = 0

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QGridLayout(self.centralWidget)
        self.setLayout(self.layout)

        self.stack = QStackedWidget(self)
        self.next = QPushButton("Next",self)
        self.flip = QPushButton("Flip",self)

        self.setStack(index)

        self.next.released.connect(self.nextCard)

        self.layout.addWidget(self.stack,0,0,2,2)
        self.layout.addWidget(self.flip,1,0,1,1)
        self.layout.addWidget(self.next,1,1,1,1)

        self.stack.show()

        self.initMenu()

        self.setFixedSize(800,600)
        self.setWindowTitle(self.flashcards[index][0].subject + " Flashcards")
        self.show()

    def setStack(self,index):
        self.index = 0
        for flashcard in self.flashcards[index]:
            self.stack.addWidget(FlashCardWidget(flashcard))
            self.index += 1
            self.maxIndex += 1

        self.maxIndex -= 1
        self.index -= 1

        self.stack.setCurrentIndex(self.index)
        self.flip.released.connect(self.stack.currentWidget().flip)

    def initMenu(self):
        self.menu = self.menuBar()
        self.file = self.menu.addMenu("&File")
        self.edit = self.menu.addMenu("&Edit")

        self.about = QAction("About",self)
        self.close = QAction("Close Window",self)
        self.create = QAction("Create Flashcard",self)
        self.delete = QAction("Delete Flashcard",self)
        self.deleteSet = QAction("Delete Flashcard Set",self)
        self.addSet = QAction("Create Flashcard Set",self)

        self.file.addAction(self.about)
        self.file.addAction(self.close)
        self.edit.addAction(self.create)
        self.edit.addAction(self.delete)
        self.edit.addAction(self.deleteSet)

    def disconnectStackCard(self):
        self.flip.released.disconnect(self.stack.widget(self.index).flip)

    def nextCard(self):
        self.flip.released.disconnect(self.stack.widget(self.index).flip)

        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.maxIndex

        self.stack.setCurrentIndex(self.index)
        self.flip.released.connect(self.stack.widget(self.index).flip)

class FlashCardCreateWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(FlashCardCreateWindow,self).__init__(*args,**kwargs)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.front = FlashCardSideView()
        self.back = FlashCardSideView()
        self.form = QFormLayout()
        self.form.addRow(QLabel("Front:"),self.front)
        self.form.addRow(QLabel("Back:"),self.back)

        self.lineEditLayout = QFormLayout()
        self.inputLayout = QHBoxLayout()
        self.subjectInput = QLineEdit()
        self.frontInput = QLineEdit()
        self.backInput = QLineEdit()
        self.done = QPushButton()

        self.lineEditLayout.addRow(QLabel("Subject:"),self.subjectInput)
        self.lineEditLayout.addRow(QLabel("Front:"),self.frontInput)
        self.lineEditLayout.addRow(QLabel("Back:"),self.backInput)

        self.inputLayout.addWidget(self.done)
        self.inputLayout.addLayout(self.lineEditLayout)

        self.layout.addLayout(self.form)
        self.layout.addLayout(self.inputLayout)

        self.setLayout(self.layout)
        self.show()

class FlashCardSideView(QWidget):
    def __init__(self,*args,**kwargs):
        super(FlashCardSideView,self).__init__(*args,**kwargs)
        self.text = QLabel()

    def setText(self,text):
        self.text.setText(text)

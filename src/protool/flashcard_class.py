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

from PySide2.QtWidgets import QStackedWidget, QLabel, QPushButton, QGridLayout, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QGridLayout, QMenu, QAction
from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtCore import Qt, Signal, Slot
import copy

class FlashCard():
    def __init__(self, subject, front_text,back_text):
        self.subject = subject
        self.front_text = front_text
        self.back_text = back_text

    def __dict__(self):
        return {
                "subject":self.subject,
                "front_text":self.front_text,
                "back_text":self.back_text
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

    def flip(self): #"flip" the flashcard by changing text shown
        if self.flipped == False:
            self.label.setText(self.flashcard.back_text)
            self.flipped = True
            return
        self.label.setText(self.flashcard.front_text)
        self.flipped = False

def sortFlashcards(flashcards): #sort flashcard into lists of subjects
    subjects = []
    for flashcard in flashcards:
        if flashcard.subject not in subjects:
            subjects.append(flashcard.subject)

            flashcardsNew = copy.deepcopy(subjects) #deepcopy so they are separate lists, very important at this stage

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

        self.stack = QStackedWidget(self) #store flashcards in a stack
        self.next = QPushButton("Next",self)
        self.flip = QPushButton("Flip",self)
        self.nextCollection = QPushButton("Next Set",self)
        self.previousCollection = QPushButton("Previous Set",self)

        self.setStack(index)

        self.next.released.connect(self.nextCard)

        self.layout.addWidget(self.stack,0,0,2,2)
        self.layout.addWidget(self.flip,1,0,1,1)
        self.layout.addWidget(self.next,1,1,1,1)
        self.layout.addWidget(self.previousCollection,2,0,1,1)
        self.layout.addWidget(self.nextCollection,2,1,1,1)

        self.stack.show()

        self.initMenu()

        self.setFixedSize(800,600)
        self.setWindowTitle(self.flashcards[index][0].subject + " Flashcards")
        self.show()

    def setStack(self,index): #set up the stack
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

        self.file.addAction(self.about)
        self.file.addAction(self.close)
        self.edit.addAction(self.create)
        self.edit.addAction(self.delete)

    def disconnectStackCard(self):
        self.flip.released.disconnect(self.stack.widget(self.index).flip)

    def nextCard(self): #go to next card weith endless scrolling
        self.flip.released.disconnect(self.stack.widget(self.index).flip)

        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.maxIndex

        self.stack.setCurrentIndex(self.index)
        self.flip.released.connect(self.stack.widget(self.index).flip)

class FlashCardCreateWindow(QMainWindow): #window to create flashcards
    def __init__(self,*args,**kwargs):
        super(FlashCardCreateWindow,self).__init__(*args,**kwargs)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.front = QLabel()
        self.back = QLabel()
        self.form = QFormLayout()
        self.form.addRow(QLabel("Front:"),self.front)
        self.form.addRow(QLabel("Back:"),self.back)

        self.lineEditLayout = QFormLayout()
        self.inputLayout = QHBoxLayout()
        self.subjectInput = QLineEdit()
        self.frontInput = QLineEdit()
        self.backInput = QLineEdit()
        self.done = QPushButton("+")

        self.frontInput.textChanged.connect(self.preview)
        self.backInput.textChanged.connect(self.preview)

        self.lineEditLayout.addRow(QLabel("Subject:"),self.subjectInput)
        self.lineEditLayout.addRow(QLabel("Front:"),self.frontInput)
        self.lineEditLayout.addRow(QLabel("Back:"),self.backInput)

        self.inputLayout.addWidget(self.done)
        self.inputLayout.addLayout(self.lineEditLayout)

        self.layout.addLayout(self.form)
        self.layout.addLayout(self.inputLayout)

        self.setLayout(self.layout)
        self.setFixedSize(400,300)
        self.setWindowTitle("Create Flashcards")
        self.show()

    def preview(self):
        self.front.setText(self.frontInput.text())
        self.back.setText(self.backInput.text())

class FlashCardDeleteWindow(QMainWindow): #window to delete flashcards
    def __init__(self,*args,**kwargs):
        super(FlashCardDeleteWindow,self).__init__(*args,**kwargs)

        self.index = 0

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)
        self.sides = QHBoxLayout()
        self.sides.setContentsMargins(0,0,0,0)
        self.buttons = QHBoxLayout()

        self.front = QLabel()
        self.back = QLabel()
        self.sides.addWidget(self.front)
        self.sides.addWidget(self.back)

        self.buttonPrevious = QPushButton("Previous")
        self.buttonConfirm =  QPushButton("Confirm")
        self.buttonNext = QPushButton("Next")
        self.buttons.addWidget(self.buttonPrevious)
        self.buttons.addWidget(self.buttonConfirm)
        self.buttons.addWidget(self.buttonNext)

        self.buttonNext.released.connect(self.nextCard)
        self.buttonPrevious.released.connect(self.previousCard)

        self.layout.addLayout(self.sides)
        self.layout.addLayout(self.buttons)

        self.setLayout(self.layout)
        self.setWindowTitle("Delete Flashcards")
        self.setFixedSize(400,300)

        self.showCard()

    def showCard(self):
        self.front.setText(flashcards[self.index].front_text)
        self.back.setText(flashcards[self.index].back_text)

    def nextCard(self):
        if self.index < len(flashcards) - 1:
            self.index += 1
        else:
            self.index = 0

        self.showCard()

    def previousCard(self):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = len(flashcards) - 1

        self.showCard()

flashcards = 0

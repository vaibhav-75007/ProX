from PySide2.QtWidgets import QStackedWidget, QLabel, QPushButton, QGridLayout, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QGridLayout, QMenu, QAction
from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtCore import Qt

class FlashCard():
    def __init__(self, subject, front_text,back_text,idNo):
        self.id = idNo
        self.subject = subject
        self.front_text = front_text
        self.back_text = back_text

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
        print("Flipped")
        print(self.label.text())
        if self.flipped == False:
            self.label.setText(self.flashcard.back_text)
            self.flipped = True
            return
        self.label.setText(self.flashcard.front_text)
        self.flipped = False

class FlashCardWindow(QMainWindow):
    def __init__(self,flashcards,*args,**kwargs):
        super(FlashCardWindow,self).__init__(*args,**kwargs)

        self.index = 0
        self.maxIndex = 0

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QGridLayout(self.centralWidget)
        self.setLayout(self.layout)

        self.stack = QStackedWidget(self)
        self.next = QPushButton("Next",self)
        self.flip = QPushButton("Flip",self)

        for flashcard in flashcards:
            self.stack.addWidget(FlashCardWidget(flashcard))
            self.index += 1
            self.maxIndex += 1

        self.maxIndex -= 1
        self.index -= 1

        self.stack.setCurrentIndex(self.index)

        self.flip.released.connect(self.stack.currentWidget().flip)
        self.next.released.connect(self.nextCard)

        self.layout.addWidget(self.stack,0,0,2,2)
        self.layout.addWidget(self.flip,1,0,1,1)
        self.layout.addWidget(self.next,1,1,1,1)

        self.stack.show()

        self.initMenu()

        self.setFixedSize(800,600)
        self.setWindowTitle("Flashcards")

    def initMenu(self):
        self.menu = self.menuBar()
        self.file = self.menu.addMenu("&File")
        self.edit = self.menu.addMenu("&Edit")
        self.view = self.menu.addMenu("&View")

        self.about = QAction("About",self)
        self.close = QAction("Close Window",self)
        self.create = QAction("Create Flashcard",self)
        self.delete = QAction("Delete Flashcard",self)
        self.deleteSet = QAction("Delete Flashcard Set",self)
        self.addSet = QAction("Create Flashcard Set",self)
        self.changeSet = QAction("View Flashcard Set",self)

        self.file.addAction(self.about)
        self.file.addAction(self.close)
        self.edit.addAction(self.create)
        self.edit.addAction(self.addSet)
        self.edit.addAction(self.delete)
        self.edit.addAction(self.deleteSet)
        self.view.addAction(self.changeSet)

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

        self.layout = QVBoxLayout()
        self.front = FlashCardSideView()
        self.back = FlashCardSideView()
        self.form = QFormLayout()
        self.form.addRow(QLabel("Front:"),self.front)
        self.form.addRow(QLabel("Back:"),self.back)

        self.lineEditLayout = QFormLayout()
        self.inputLayout = QHBoxLayout()
        self.frontInput = QLineEdit()
        self.backInput = QLineEdit()
        self.done = QPushButton()

        self.lineEditLayout.addRow(QLabel("Front:"),self.frontInput)
        self.lineEditLayout.addRow(QLabel("Back:"),self.backInput)

        self.inputLayout.addWidget(self.done)
        self.inputLayout.addLayout(self.lineEditLayout)

        self.layout.addLayout(self.form)
        self.layout.addLayout(self.inputLayout)

        self.setLayout(self.layout)

class FlashCardSideView(QWidget):
    def __init__(self,*args,**kwargs):
        super(FlashCardSideView,self).__init__(*args,**kwargs)
        self.text = QLabel()

    def setText(self,text):
        self.text.setText(text)

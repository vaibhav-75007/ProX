from PySide2.QtWidgets import QStackedWidget, QLabel, QPushButton, QGridLayout, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit
from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtCore import Qt

class FlashCard():
    def __init__(self, subject, front_text,back_text):
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
        if self.flipped == False:
            self.label.setText(self.flashcard.back_text)
            return
        self.label.setText(self.flashcard.front_text)

class FlashCardWindow(QMainWindow):
    def __init__(self,flashcards,*args,**kwargs):
        super(FlashCardWindow,self).__init__(*args,**kwargs)

        self.stack = QStackedWidget(self)

        self.setCentralWidget(self.stack)

        for flashcard in flashcards:
            self.stack.addWidget(FlashCardWidget(flashcard))

        self.stack.show()

        self.setFixedSize(800,600)
        self.setWindowTitle("Flashcards")

    def nextCard(self):
       pass

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

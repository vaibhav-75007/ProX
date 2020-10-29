# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QMainWindow,QLineEdit,QFormLayout,QDialogButtonBox,QWidget


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

    def addTopic(self,topic):
        if topic not in self.topics:
            self.topics.append(topic)

    def deleteTopic(self,topic):
        self.topics.remove(topic)

class CurriculumWindow(QMainWindow):
    pass

class CurriculumWidget(QWidget):
    pass

curriculums = 0

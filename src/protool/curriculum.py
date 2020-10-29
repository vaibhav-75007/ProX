# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets


class Curriculum:
    def __init__(self,name,subject,topics):
        self.name = naem
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

#create widget for curriculums view

curriculums = 0

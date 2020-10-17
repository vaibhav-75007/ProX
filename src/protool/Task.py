# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListWidgetItem, QListWidget, QCheckBox
from PySide2.QtGui import QColor, QBrush, QLinearGradient
from datetime import datetime


class Task:
    def __init__(self,deadline,name,description,priority):
        self.deadline = deadline
        self.name = name
        self.description = description
        self.isComplete = False
        self.isOverdue = False
        self.priority = priority

    def getDeadline(self):
        return self.deadline

    def checkOverdue(self):
        if datetime.now() > deadline:
            isOverdue = True

    def complete(self):
        self.isComplete = True

class TaskWidget(QListWidgetItem):
    def __init__(self,task,*args,**kwargs):
        super(TaskWidget,self).__init__(*args,**kwargs)

        gradient = QLinearGradient(0,0,650,650)

        self.task = task

        self.text = '\t' + self.task.name + '\n\t' + str(self.task.getDeadline()) + '\n\t' + self.task.description

        self.setText(self.text)

        if self.task.priority == True:
            gradient.setColorAt(0,QColor.fromRgbF(1,0,0,1))
            gradient.setColorAt(1,QColor.fromRgbF(1,0,1,0.1))
        else:
            gradient.setColorAt(0,QColor.fromRgbF(0,0.7,1,0.8))
            gradient.setColorAt(1,QColor.fromRgbF(1,0,1,0.1))


        brush = QBrush(gradient)
        self.setBackground(brush)

        text = QBrush(QColor.fromRgbF(0.9,0.9,0.9,1))
        self.setForeground(text)

class ToDoList(QListWidget):
    def __init__(self,tasks,*args,**kwargs):
        super(ToDoList,self).__init__(*args,**kwargs)
        for task in tasks:
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.setItemWidget(self.item(i), QCheckBox())

        self.show()

# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListWidgetItem, QListWidget, QCheckBox
from datetime import datetime


class Task:
    def __init__(self,deadline,name,description):
        self.deadline = deadline
        self.name = name
        self.description = description
        self.isComplete = False
        self.isOverdue = False

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

        self.task = task

        self.text = self.task.name + '\n' + str(self.task.getDeadline()) + '\n' + self.task.description

        self.setText(self.text)

class ToDoList(QListWidget):
    def __init__(self,tasks,*args,**kwargs):
        super(ToDoList,self).__init__(*args,**kwargs)
        for task in tasks:
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.setItemWidget(self.item(i), QCheckBox())

        self.show()

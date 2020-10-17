# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListWidgetItem, QListWidget, QCheckBox, QWidget, QHBoxLayout, QFormLayout, QLabel, QSpinBox, QLineEdit
from PySide2.QtGui import QColor, QBrush, QLinearGradient
from datetime import datetime


class Task:
    def __init__(self,deadline,name,description):
        self.deadline = deadline
        self.name = name
        self.description = description
        self.isComplete = False
        self.isOverdue = False
        self.priority = False

        now = datetime.now()

        if now > deadline:
            self.isOverdue = True

        if datetime(now.year,now.month,now.day + 7) > deadline:
            self.priority = True

    def getDeadline(self):
        return self.deadline

    def complete(self):
        self.isComplete = True

class TaskWidget(QListWidgetItem):
    def __init__(self,task,*args,**kwargs):
        super(TaskWidget,self).__init__(*args,**kwargs)

        gradient = QLinearGradient(0,0,650,650) #create gradient color for task

        self.task = task

        self.text = '\t' + self.task.name + '\n\t' + str(self.task.getDeadline()) + '\n\t' + self.task.description

        self.setText(self.text)

        if self.task.priority == True: #change color to red if high priority
            gradient.setColorAt(0,QColor.fromRgbF(1,0,0,1))
            gradient.setColorAt(1,QColor.fromRgbF(1,0,1,0.1))
        else: #change color to blue if low priority
            gradient.setColorAt(0,QColor.fromRgbF(0,0.7,1,0.8))
            gradient.setColorAt(1,QColor.fromRgbF(1,0,1,0.1))


        brush = QBrush(gradient)
        self.setBackground(brush)

        text = QBrush(QColor.fromRgbF(0.9,0.9,0.9,1))
        self.setForeground(text)

class ToDoList(QListWidget):
    def __init__(self,tasks,*args,**kwargs):
        super(ToDoList,self).__init__(*args,**kwargs)
        tasks = self.sortTasks(tasks)

        for task in tasks:
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.setItemWidget(self.item(i), QCheckBox()) #add a checkbox to make complete

        self.show()

    def sortTasks(self,tasks):
        tasks.sort(key=lambda t: t.deadline)
        return tasks

class TaskInputFieldWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super(TaskInputFieldWidget,self).__init__(*args,**kwargs)

        self.layout = QFormLayout(self)
        self.deadlineInputLayout = QHBoxLayout()
        self.deadlineInputYear = QSpinBox()
        self.deadlineInputMonth = QSpinBox()
        self.deadlineInputDay = QSpinBox()

        self.deadlineLabelYear = QLabel("YYYY")
        self.deadlineLabelMonth = QLabel("MM")
        self.deadlineLabelDay = QLabel("DD")

        self.deadlineInputLayout.addWidget(self.deadlineLabelYear)
        self.deadlineInputLayout.addWidget(self.deadlineInputYear)
        self.deadlineInputLayout.addWidget(self.deadlineLabelMonth)
        self.deadlineInputLayout.addWidget(self.deadlineInputMonth)
        self.deadlineInputLayout.addWidget(self.deadlineLabelDay)
        self.deadlineInputLayout.addWidget(self.deadlineInputDay)

        self.nameInput = QLineEdit()
        self.descriptionInput = QLineEdit()

        self.nameLabel = QLabel("Name:")
        self.descriptionLabel = QLabel("Description:")
        self.deadlineLabel = QLabel("Deadline:")

        self.layout.addRow(self.nameLabel,self.nameInput)
        self.layout.addRow(self.descriptionLabel,self.descriptionInput)
        self.layout.addRow(self.deadlineLabel,self.deadlineInputLayout)

        self.setLayout(self.layout)

        self.show()

    def createNewTask(self):
        pass

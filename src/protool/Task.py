# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListWidgetItem, QListWidget, QCheckBox, QWidget, QHBoxLayout, QFormLayout, QLabel, QSpinBox, QLineEdit, QPushButton
from PySide2.QtGui import QColor, QBrush, QLinearGradient, QPalette
from PySide2.QtCore import Signal, Slot
from datetime import datetime


class Task:
    def __init__(self,deadline,name,description,idNo):
        self.id = idNo
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

        self.text = f'\t{self.task.getDeadline().year}/{self.task.getDeadline().month}/{self.task.getDeadline().day}\n\t{self.task.name}\n\t{self.task.description}'

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
        self.tasks = self.sortTasks(tasks)

        for task in self.tasks:
            self.addItem(TaskWidget(task))

        self.checkBoxes = []

        for i in range(self.count()):
            self.checkBoxes.append(QCheckBox())
            self.checkBoxes[i].stateChanged.connect(self.removeTask)
            self.setItemWidget(self.item(i), self.checkBoxes[i]) #add a checkbox to make complete

        self.show()

    def sortTasks(self,tasks):
        tasks.sort(key=lambda t: t.deadline)
        return tasks

    def removeTask(self):
        index = -1
        for i in range(len(self.checkBoxes)):
            if self.checkBoxes[i].isChecked() == True:
                index = i

        if index == -1:
            return

        print(index)
        print("List len: " + str(self.count()))
        print("Checkboxes len: " + str(len(self.checkBoxes)))
        print("Tasks len: " + str(len(self.tasks)))
        self.takeItem(index)
        self.checkBoxes.pop(index)
        self.tasks.pop(index)

        for i in range(self.count()):
            self.checkBoxes[i].stateChanged.connect(self.removeTask)

        print("Finished")
        return

    @Slot(Task)
    def addTask(self,task):
        if task.name == "" or task.description == "":
            return

        self.tasks.append(task)

        for j in range(3):
            for i in range(self.count()):
                item = self.takeItem(i)

        self.tasks = self.sortTasks(self.tasks)
        self.checkBoxes.clear()

        for task in self.tasks:
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.checkBoxes.append(QCheckBox())
            self.setItemWidget(self.item(i), self.checkBoxes[i])
            self.checkBoxes[i].stateChanged.connect(self.removeTask)

class TaskInputFieldWidget(QWidget):
    add = Signal(Task)

    def __init__(self,*args,**kwargs):
        super(TaskInputFieldWidget,self).__init__(*args,**kwargs)

        self.setForegroundRole(QPalette.Text)

        palette = QPalette()
        palette.setBrush(QPalette.Text,QBrush(QColor.fromRgbF(0.9,0.9,0.9,1)))
        self.mainlayout = QHBoxLayout(self)

        self.layout = QFormLayout()
        self.deadlineInputLayout = QHBoxLayout()
        self.deadlineInputYear = QSpinBox()
        self.deadlineInputMonth = QSpinBox()
        self.deadlineInputDay = QSpinBox()

        self.deadlineInputYear.setMaximum(3000)
        self.deadlineInputYear.setMinimum(2020)
        self.deadlineInputMonth.setMaximum(12)
        self.deadlineInputMonth.setMinimum(1)
        self.deadlineInputDay.setMaximum(31)
        self.deadlineInputDay.setMinimum(1)

        self.deadlineLabelYear = QLabel("<font color=white>YYYY</font>")
        self.deadlineLabelMonth = QLabel("<font color=white>MM</font>")
        self.deadlineLabelDay = QLabel("<font color=white>DD</font>")

        self.deadlineInputLayout.addWidget(self.deadlineLabelYear)
        self.deadlineInputLayout.addWidget(self.deadlineInputYear)
        self.deadlineInputLayout.addWidget(self.deadlineLabelMonth)
        self.deadlineInputLayout.addWidget(self.deadlineInputMonth)
        self.deadlineInputLayout.addWidget(self.deadlineLabelDay)
        self.deadlineInputLayout.addWidget(self.deadlineInputDay)

        self.nameInput = QLineEdit()
        self.descriptionInput = QLineEdit()

        self.nameLabel = QLabel("<font color=white>Name:</font>")
        self.descriptionLabel = QLabel("<font color=white>Description:</font>")
        self.deadlineLabel = QLabel("<font color=white>Deadline:</font>")

        self.layout.addRow(self.nameLabel,self.nameInput)
        self.layout.addRow(self.descriptionLabel,self.descriptionInput)
        self.layout.addRow(self.deadlineLabel,self.deadlineInputLayout)

        self.done = QPushButton()
        self.mainlayout.addWidget(self.done)
        self.mainlayout.addLayout(self.layout)
        self.setLayout(self.mainlayout)

        self.show()

    def inputToDate(self):
        return datetime(self.deadlineInputYear.value(),self.deadlineInputMonth.value(),self.deadlineInputDay.value())

    def createTask(self):
        task = Task(self.inputToDate(),self.nameInput.text(),self.descriptionInput.text())
        self.nameInput.clear()
        self.descriptionInput.clear()
        self.deadlineInputYear.setValue(datetime.now().year)
        self.deadlineInputMonth.setValue(datetime.now().month)
        self.deadlineInputDay.setValue(datetime.now().day)

        self.add.emit(task)

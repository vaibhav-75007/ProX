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

# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListWidgetItem, QListWidget, QCheckBox, QWidget, QHBoxLayout, QFormLayout, QLabel, QSpinBox, QLineEdit, QPushButton
from PySide2.QtGui import QColor, QBrush, QLinearGradient, QPalette
from PySide2.QtCore import Signal, Slot
import datetime
import jsonUtil as js
import user_class as user
import flashcard_class as flash
import curriculum

class Task:
    def __init__(self,deadline,name,description):
        self.deadline = deadline
        self.name = name
        self.description = description
        self.isComplete = False
        self.isOverdue = False
        self.priority = False

        now = datetime.datetime.now()

        if now > deadline: #check if overdue
            self.isOverdue = True

        if deadline - datetime.datetime(now.year,now.month,now.day) < datetime.timedelta(days=7): #check if deadline is soon
            self.priority = True

    def __dict__(self): #convert to dictionary to easily write to json
        return {
                "name":self.name,
                "description":self.description,
                "deadline":str(self.deadline.year) + '/' + str(self.deadline.month) + '/' + str(self.deadline.day) + ' 23:59:59'
               }

    def getDeadline(self):
        return self.deadline

class TaskWidget(QListWidgetItem): #class for showing tasks
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

class ToDoList(QListWidget): #todo list calss
    def __init__(self,tasks,*args,**kwargs):
        super(ToDoList,self).__init__(*args,**kwargs)

        if len(tasks) == 0: #make sure tasks are only shown if they are there
            self.tasks = []
            self.checkBoxes = []
            return

        self.tasks = self.sortTasks(tasks) #sort tasks by priority
        self.checkBoxes = [] #keep checkboxes for each task

        for task in self.tasks:
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.checkBoxes.append(QCheckBox())
            self.checkBoxes[i].stateChanged.connect(self.removeTask)
            self.setItemWidget(self.item(i), self.checkBoxes[i]) #add a checkbox to make complete

        self.show()

    def sortTasks(self,tasks):
        tasks.sort(key=lambda t: t.deadline) #lambda to sort tasks by deadline
        return tasks

    def removeTask(self): #remove a task
        index = -1
        for i in range(len(self.checkBoxes)): #find which task has been completed
            if self.checkBoxes[i].isChecked() == True:
                index = i

        if index == -1: #if no task completed then return
            return

        if self.tasks[index].isOverdue: #if task is overdue increase the deadlines missed by one
            user.user.increase_deadlines_missed(1)
            user.user.increase_week_deadline_missed(1)

        self.takeItem(index) #remove the item, checkbox and the task from the json
        self.checkBoxes.pop(index)
        self.tasks.remove(self.tasks[index])
        tasks = self.tasks
        user.user.increase_task_completion_rate(1) #increase task completion rate
        user.user.increase_week_task_completion_rate(1)

        user.user.productivity_score = calcProScore(user.user.task_completion_rate,user.user.deadlines_missed) #recalculate productivity metrics
        user.user.week_productivity_score = calcProScore(user.user.week_task_completion_rate,user.user.week_deadline_missed)

        if len(tasks) == 0: #make sure to end function if tasks are empty to avoid array out of bounds errors
            js.writeAll(user.user,curriculum.curriculums,tasks,flash.flashcards)
            return

        js.writeAll(user.user,curriculum.curriculums,tasks,flash.flashcards) #rewrite to json and db if online

        for i in range(self.count()): #reconnect the checkboxes
            self.checkBoxes[i].stateChanged.connect(self.removeTask)

        return

    @Slot(Task) #this function takes a task parameter
    def addTask(self,task):    
        if task.name == "" or task.description == "": #presence check
            return

        self.tasks.append(task) #add the task to the list and write to the json
        #tasks.append(task)
        js.writeAll(user.user,curriculum.curriculums,tasks,flash.flashcards)

        for j in range(3): #reset the list (not sure why but doing just one iteration doesnt work, requires 3 to remove all tasks)
            for i in range(self.count()):
                item = self.takeItem(i)

        self.tasks = self.sortTasks(self.tasks) #resort the tasks
        self.checkBoxes.clear() #clear the checkboxes

        for task in self.tasks: #repopulate the tasks and checkboxes
            self.addItem(TaskWidget(task))

        for i in range(self.count()):
            self.checkBoxes.append(QCheckBox())
            self.setItemWidget(self.item(i), self.checkBoxes[i])
            self.checkBoxes[i].stateChanged.connect(self.removeTask)

class TaskInputFieldWidget(QWidget):
    add = Signal(Task) #signal to create task

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

        self.deadlineInputMonth.valueChanged.connect(self.changeDateMaximum) #make sure to change date maximum depending on month and/or leap year
        self.deadlineInputYear.valueChanged.connect(self.changeDateMaximum)

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

        self.done = QPushButton("+")
        self.mainlayout.addWidget(self.done)
        self.mainlayout.addLayout(self.layout)
        self.setLayout(self.mainlayout)

        self.show()

    def changeDateMaximum(self): #make sure all dates entered must be valid
        value = 31
        month = self.deadlineInputMonth.value()
        year = self.deadlineInputYear.value()
        if month == 2 and year % 4 != 0:
            value = 28
        elif month == 2 and year % 4 == 0:
            value = 29
        elif month == 4 or month == 6 or month == 9 or month == 11:
            value = 30
        self.deadlineInputDay.setMaximum(value)

    def inputToDate(self): #convert input to datetime
        return datetime.datetime(self.deadlineInputYear.value(),self.deadlineInputMonth.value(),self.deadlineInputDay.value())

    def createTask(self): #create the task
        task = Task(self.inputToDate(),self.nameInput.text(),self.descriptionInput.text())
        self.nameInput.clear() #clear/reset all the inputs
        self.descriptionInput.clear()
        self.deadlineInputYear.setValue(datetime.datetime.now().year)
        self.deadlineInputMonth.setValue(datetime.datetime.now().month)
        self.deadlineInputDay.setValue(datetime.datetime.now().day)

        self.add.emit(task) #put task in todo list

tasks = 0

def calcProScore(taskCompletion,missedDeadlines): #productivity score is taskCompletion / missedDeadline converted to an int
    if missedDeadlines == 0:
        return taskCompletion
    else:
        return int(taskCompletion / missedDeadlines)

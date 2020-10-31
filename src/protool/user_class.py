from PySide2.QtWidgets import QListWidgetItem, QListWidget
from PySide2.QtGui import QColor, QBrush, QPalette

class User():
    def __init__(self,name,productivity_score,task_completion_rate,deadlines_missed,week_productivity_score,week_task_completion_rate,week_deadline_missed,idNo,email,pin):
        self.id = idNo
        self.name = name
        self.productivity_score = productivity_score
        self.task_completion_rate = task_completion_rate
        self.deadlines_missed = deadlines_missed
        self.week_productivity_score = week_productivity_score
        self.week_task_completion_rate = week_task_completion_rate
        self.week_deadline_missed = week_deadline_missed
        self.email = email
        self.pin = pin

    def __dict__(self):
        return {
                "id":self.id,
                "name":self.name,
                "email":self.email,
                "pin":self.pin,
                "productivity_score":self.productivity_score,
                "task_completion_rate":self.task_completion_rate,
                "missed_deadline":self.deadlines_missed,
                "weekly_productivity_score":self.week_productivity_score,
                "weekly_task_completion_rate":self.week_task_completion_rate,
                "weekly_deadlines_missed":self.week_deadline_missed
               }
    
    def change_name(self,string):
        self.name =string 

    def increase_productivity_score(self, score):
        self.productivity_score += score 
    
    def decrease_productivity_score(self, score):
        self.productivity_score -= score
    
    def increase_task_completion_rate(self,score):
        self.task_completion_rate += score
    
    def decrease_task_completion_rate(self,score):
        self.task_completion_rate-=score
    
    def increase_deadlines_missed(self,score):
        self.deadlines_missed += score
    
    def decrease_deadlines_missed(self,score):
        self.deadlines_missed -= score

    def increase_week_productivity_score(self,score):
        self.week_productivity_score +=score

    def decrease_week_productivity_score(self,score):
        self.week_productivity_score -= score

    def increase_week_task_completion_rate(self,score):
        self.week_task_completion_rate+= score

    def decrease_week_task_completion_rate(self,score):
        self.week_task_completion_rate-= score

    def increase_week_deadline_missed(self,score):
        self.week_deadline_missed+= score

    def  decrease_week_deadline_missed(self,score):
        self.week_deadline_missed-= score

class UserListItem(QListWidgetItem): #stores user data in neat item to store in leaderboard
    def __init__(self, user, *args, **kwargs):
        super(UserListItem,self).__init__(*args,**kwargs)

        self.formattedText = { #format the text
        "name": "Username: " + user.name + '\n',
        "proScore": "Productivity Score: " + str(user.productivity_score) + '\n',
        "taskComp": "Tasks Completed: " + str(user.task_completion_rate) + '\n',
        "deadMissed": "Deadlines Missed: " + str(user.deadlines_missed) + '\n',
        "weekPro": "Productivity Score This Week: " + str(user.week_productivity_score) + '\n',
        "weekTaskComp": "Tasks Completed This Week: " + str(user.week_task_completion_rate) + '\n',
        "weekDeadMissed": "Missed Deadlines This Week: " + str(user.week_deadline_missed) + '\n'
        }

        self.stringText = ""
        for i in self.formattedText:
            self.stringText += self.formattedText[i]

        self.setText(self.stringText)

        self.user = user

        brush = QBrush(QColor.fromRgbF(0.4,0.4,0.4))
        self.setBackground(brush)

        text = QBrush(QColor.fromRgbF(0.9,0.9,0.9,1))
        self.setForeground(text)

    def getProScore(self):
        return self.user.productivity_score

    def getProWeekScore(self):
        return self.user.week_productivity_score

class LeaderBoard(QListWidget): #list widget to store the users, only refreshes when app restarts
    def __init__(self, users, parent, *args, **kwargs):
        super(LeaderBoard,self).__init__(parent=parent,*args,**kwargs)
        for user in users:
            self.addItem(UserListItem(user))

        self.setBackgroundRole(QPalette.Window)

        palette = QPalette()
        palette.setBrush(QPalette.Window,QBrush(QColor.fromRgbF(0.3,0.3,0.3,1)))

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.show()

user = 0

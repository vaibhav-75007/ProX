from PySide2.QtWidgets import QListWidgetItem, QListWidget

class User():

    def __init__(self,name,productivity_score,task_completion_rate,deadlines_missed,week_productivity_score,week_task_completion_rate,week_deadline_missed ):
        self.name = name
        self.productivity_score = productivity_score
        self.task_completion_rate = task_completion_rate
        self.deadlines_missed = deadlines_missed
        self.week_productivity_score = week_productivity_score
        self.week_task_completion_rate = week_task_completion_rate
        self.week_deadline_missed = week_deadline_missed
    
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

class UserListItem(QListWidgetItem):
    def __init__(self, user, *args, **kwargs):
        super(UserListItem,self).__init__(*args,**kwargs)

        self.formattedText = {
        "name": "Username: " + user.name + '\n',
        "proScore": "Productivity Score: " + str(user.productivity_score) + '\n',
        "taskComp": "Task Completion Rate: " + str(user.task_completion_rate) + '\n',
        "deadMissed": "Deadlines Missed: " + str(user.deadlines_missed) + '\n',
        "weekPro": "Weekly Productivity Score: " + str(user.week_productivity_score) + '\n',
        "weekTaskComp": "Weekly Task Completion: " + str(user.week_task_completion_rate) + '\n',
        "weekDeadMissed": "Weekly Missed Deadlines: " + str(user.week_deadline_missed) + '\n'
        }

        self.stringText = ""
        for i in self.formattedText:
            self.stringText += self.formattedText[i]

        self.setText(self.stringText)

        self.user = user

    def getProScore(self):
        return self.user.productivity_score

    def getProWeekScore(self):
        return self.user.week_productivity_score

class LeaderBoard(QListWidget):
    def __init__(self, users, parent, *args, **kwargs):
        super(LeaderBoard,self).__init__(parent=parent,*args,**kwargs)
        for user in users:
            self.addItem(UserListItem(user))

        self.show()

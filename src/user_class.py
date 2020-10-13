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

    

class FlashCard(object):

    def __init__(self, subject, front_text,back_text):
        self.subject = subject
        self.front_text = front_text
        self.back_text =back_text

    def change_subject(self, text):
        self.subject = text

    def change_front_text(self,text):
        self.front_text = text
    
    def change_back_text(self,text):
        self.back_text = text


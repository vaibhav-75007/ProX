# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout, QDialogButtonBox


class InfoDialog(QDialog):
    def __init__(self,*args,**kwargs):
        super(InfoDialog,self).__init__(*args,**kwargs)
        #initialise the parent QDialog
        self.text = QPlainTextEdit(self) #create a text edit to show the about section
        self.text.setPlainText("About this app:\nCreated by:")

        self.dialog = QDialogButtonBox(QDialogButtonBox.Ok)
        self.dialog.accepted.connect(self.close) #create a button to close the dialog

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.dialog)
        self.setLayout(self.layout) #set everythin in a vertical layout


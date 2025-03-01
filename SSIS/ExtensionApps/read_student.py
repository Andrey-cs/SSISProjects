# FOR READ FUNCTION

from PyQt5.QtWidgets import QDialog
from read_data import Ui_Dialog

class ReadStudent(QDialog, Ui_Dialog):
    def __init__(self, student_data):
        super().__init__()
        self.setupUi(self)
        self.student_data = student_data
        self.populate_fields()

    def populate_fields(self):
        self.studentIDLineEdit.setText(self.student_data["Student ID"])
        self.firstNameLineEdit.setText(self.student_data["First Name"])
        self.lastNameLineEdit.setText(self.student_data["Last Name"])
        self.ageLineEdit.setText(str(self.student_data["Age"]))
        self.sexComboBox.setCurrentText(self.student_data["Sex"])
        self.programComboBox.setCurrentText(self.student_data["Program"])
        self.yearLevelLineEdit.setText(str(self.student_data["Year Level"]))
        self.collegeComboBox.setCurrentText(self.student_data["College"])

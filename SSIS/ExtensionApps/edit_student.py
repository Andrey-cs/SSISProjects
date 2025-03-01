# FOR EDIT FUNCTION

from PyQt5.QtWidgets import QDialog
from edit_data import Ui_Dialog
from database.database import update_student

class EditStudent(QDialog, Ui_Dialog):
    def __init__(self, student_data):
        super().__init__()
        self.setupUi(self)
        self.student_data = student_data
        self.populate_fields()
        self.saveButton.clicked.connect(self.save_changes)

    def populate_fields(self):
        self.studentIDLineEdit.setText(self.student_data["Student ID"])
        self.firstNameLineEdit.setText(self.student_data["First Name"])
        self.lastNameLineEdit.setText(self.student_data["Last Name"])
        self.ageLineEdit.setText(str(self.student_data["Age"]))
        self.sexComboBox.setCurrentText(self.student_data["Sex"])
        self.programComboBox.setCurrentText(self.student_data["Program"])
        self.yearLevelLineEdit.setText(str(self.student_data["Year Level"]))
        self.collegeComboBox.setCurrentText(self.student_data["College"])

    def save_changes(self):
        updated_data = {
            "First Name": self.firstNameLineEdit.text(),
            "Last Name": self.lastNameLineEdit.text(),
            "Age": int(self.ageLineEdit.text()),
            "Sex": self.sexComboBox.currentText(),
            "Program": self.programComboBox.currentText(),
            "Year Level": int(self.yearLevelLineEdit.text()),
            "College": self.collegeComboBox.currentText()
        }
        update_student(self.student_data["Student ID"], updated_data)
        self.close()

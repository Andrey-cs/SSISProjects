# app.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from mainFINALE import Ui_Form
from database.database import *
from extensionapplications.read_student import ReadStudent
from extensionapplications.edit_student import EditStudent

class MainApp(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Load programs and colleges
        self.programs = load_programs()
        self.colleges = load_colleges()
        
        # Connect buttons
        self.addButton.clicked.connect(self.add_student)
        self.readButton.clicked.connect(self.read_student)
        self.updateButton.clicked.connect(self.update_student)
        self.deleteButton.clicked.connect(self.delete_student)
        self.clearButton.clicked.connect(self.clear_fields)
        self.editButton.clicked.connect(self.edit_student)
        
        # Populate program combo box
        self.programComboBox.addItems(self.programs["Program Code"] + " - " + self.programs["Program Name"])
        
        # Connect program selection to college update
        self.programComboBox.currentIndexChanged.connect(self.update_college)

        # Initialize student list
        self.update_list()

    def update_college(self):
        selected_program = self.programComboBox.currentText().split(" - ")[0]
        college_info = self.programs[self.programs["Program Code"] == selected_program]
        self.collegeComboBox.setCurrentText(college_info["College Code"].values[0] + " - " + college_info["College Name"].values[0])

    def add_student(self):
        student_data = {
            "Student ID": self.studentIDLineEdit.text(),
            "First Name": self.firstNameLineEdit.text(),
            "Last Name": self.lastNameLineEdit.text(),
            "Age": int(self.ageLineEdit.text()),
            "Sex": self.sexComboBox.currentText(),
            "Program": self.programComboBox.currentText().split(" - ")[0],
            "Year Level": int(self.yearLevelLineEdit.text()),
            "College": self.collegeComboBox.currentText().split(" - ")[0]
        }
        add_student(student_data)
        self.update_list()

    def read_student(self):
        selected_student = self.get_selected_student()
        if selected_student:
            self.read_window = ReadStudent(selected_student)
            self.read_window.show()

    def update_student(self):
        selected_student = self.get_selected_student()
        if selected_student:
            updated_data = {
                "First Name": self.firstNameLineEdit.text(),
                "Last Name": self.lastNameLineEdit.text(),
                "Age": int(self.ageLineEdit.text()),
                "Sex": self.sexComboBox.currentText(),
                "Program": self.programComboBox.currentText().split(" - ")[0],
                "Year Level": int(self.yearLevelLineEdit.text()),
                "College": self.collegeComboBox.currentText().split(" - ")[0]
            }
            update_student(selected_student["Student ID"], updated_data)
            self.update_list()

    def delete_student(self):
        selected_student = self.get_selected_student()
        if selected_student:
            delete_student(selected_student["Student ID"])
            self.update_list()

    def clear_fields(self):
        self.studentIDLineEdit.clear()
        self.firstNameLineEdit.clear()
        self.lastNameLineEdit.clear()
        self.ageLineEdit.clear()
        self.sexComboBox.setCurrentIndex(0)
        self.programComboBox.setCurrentIndex(0)
        self.yearLevelLineEdit.clear()
        self.collegeComboBox.clear()

    def edit_student(self):
        selected_student = self.get_selected_student()
        if selected_student:
            self.edit_window = EditStudent(selected_student)
            self.edit_window.show()

    def get_selected_student(self):
        selected_row = self.studentTable.currentRow()
        if selected_row >= 0:
            student_id = self.studentTable.item(selected_row, 0).text()
            return get_student(student_id)
        return None

    def update_list(self):
        students = list_students()
        self.studentTable.setRowCount(len(students))
        for i, student in enumerate(students.to_dict("records")):
            for j, key in enumerate(student.keys()):
                self.studentTable.setItem(i, j, QTableWidgetItem(str(student[key])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
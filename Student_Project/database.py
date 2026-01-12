# FILE: database.py
import json
import os
from model import Student  # model.py mathi Student class import karyo

DB_FILE = "students.json"

class Database:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        """JSON file mathi data lavshe"""
        if not os.path.exists(DB_FILE):
            return

        try:
            with open(DB_FILE, "r") as f:
                data_list = json.load(f)
                # Darek dictionary ne Student object ma convert kare che
                self.students = [Student.from_dict(d) for d in data_list]
        except Exception:
            self.students = []

    def save_data(self):
        """Data ne JSON file ma save karshe"""
        data_list = [s.to_dict() for s in self.students]
        with open(DB_FILE, "w") as f:
            json.dump(data_list, f, indent=4)

    def add_student(self, name, course):
        # Auto-increment Roll Number logic
        new_roll = 1
        if self.students:
            new_roll = self.students[-1].roll_no + 1
        
        new_student = Student(new_roll, name, course)
        self.students.append(new_student)
        self.save_data()
        return new_student

    def get_all_students(self):
        return self.students

    def delete_student(self, roll_no):
        initial_count = len(self.students)
        # Filter logic: Je roll number match na thay e rakhiyu
        self.students = [s for s in self.students if s.roll_no != roll_no]
        
        if len(self.students) < initial_count:
            self.save_data()
            return True
        return False
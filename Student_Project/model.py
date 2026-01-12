# FILE: model.py

class Student:
    def __init__(self, roll_no, name, course):
        self.roll_no = roll_no
        self.name = name
        self.course = course

    # Object ne Dictionary (JSON format) ma fervava mate
    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "course": self.course
        }

    # Dictionary mathi pacho Object banavva mate (Static Method)
    @staticmethod
    def from_dict(data):
        return Student(data["roll_no"], data["name"], data["course"])

    def __str__(self):
        return f"🆔 {self.roll_no} | 👤 {self.name} | 📚 {self.course}"
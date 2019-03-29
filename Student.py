
class Student:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.grades = {}
        self.attendence = {}

    def add_grade(self, course_name, grade):
        self.grades[course_name].append(grade)

    def add_attendence(self, date, attendece):
        self.attendence[date] = attendence

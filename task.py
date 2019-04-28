import uuid
from uuid import UUID
from datetime import datetime
import json

class Student:

    def __init__(self, name, surname, courses, Id=None):
        if Id == None:
            self.id = int(uuid.uuid4())
        else:
            self.id = int(Id)
        self.name = name
        self.surname = surname
        self.courses = courses
    
    def to_json(self):
        return {'id': self.id}

    # def add_grade_by_course(self, course, grade):
    #     for i in self.courses:
    #         if i == course

    def add_course(self, course):
        self.courses.append(course)
        print(course.course_name)
        course.add_student(self.id)


    def get_total_avg(self):
        soma = 0
        for course in self.courses:
            soma += course.get_avg_by_student(self.id)
        
        return soma/len(self.courses)
    
    def get_list_positive_courses(self):
        lista = list(filter(lambda x: x.get_avg_by_student(self.id) >= 9.5, self.courses))
        final = []
        for i in lista:
            final.append(i.course_name)
        return final



class Student_Course_score:

    def __init__(self, student_id, course_name):
        self.grades = []
        self.attendance = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def set_attendance(self, date):
        self.attendance.append(date)

    def get_attendance(self):
        return len(self.attendance)            

    def get_avg(self):
        return sum(self.grades,0)/len(self.grades)


class Classroom:
    def __init__(self, course_name, grades, attendance):
        self.course_name = course_name
        if grades != None:
            self.student_grades = grades
        else:
            self.student_grades = {}
        if attendance != None:
            self.student_attendance = attendance
        else:
            self.student_attendance = {}
    
    def add_student(self, student_id):
        self.student_grades[student_id] = []
        self.student_attendance[student_id] = []

    def add_grade(self, student_id, grade):
        self.student_grades[student_id].append(grade)

    def add_attendance(self, student_id, date):
        self.student_attendance[student_id].append(date)

    def get_avg_by_student(self, student_id):
        return sum(self.student_grades[student_id])/len(self.student_grades[student_id])

    def get_total_avg(self):
        soma = 0
        keys = self.student_grades.keys()
        for key in keys:
            soma += self.get_avg_by_student(key)
        return soma/len(keys)

    def get_attendance_by_student(self, student_id):
        return len(self.student_attendance[student_id])

    def get_higher_score(self):
        keys = self.student_grades.keys()
        max_grade = 0
        for key in keys:
            grade = self.get_avg_by_student(key)
            if  grade > max_grade:
                max_grade = grade

        return max_grade

    def get_best_students(self):
        keys = self.student_grades.keys()
        return list(filter(lambda x: self.get_avg_by_student(x) == self.get_higher_score() , keys))


if __name__ == '__main__':

    json_file = open('Student.json', 'r')
    data = json.load(json_file)

    classroom = open('Classes.json', 'r')
    data2 = json.load(classroom)

    number_class = len(data2['classes'])
    number_std = len(data['students'])

    list_classes = []
    list_students = []
    lista = {}
    conta = 0
    for k in data2['classes']:
        notas = {}
        presenca = {}
        for i in range(number_std):
            
            lista[data['students'][i]['id']] = data['students'][i]['course']
            classes = []
            
            for j in range(len(lista[data['students'][i]['id']])):
                classes.append(['course_name'])
                if k == lista[data['students'][i]['id']][j]['course_name']:
                    notas[data['students'][i]['id']] = lista[data['students'][i]['id']][j]['grades']
                    presenca[data['students'][i]['id']] = lista[data['students'][i]['id']][j]['attendance']

        list_classes.append(Classroom(k, notas, presenca))


    for i in range(number_std):
        initial_courses = []
        for k in range(len(list_classes)):
            for j in range(len(lista[data['students'][i]['id']])):
                if list_classes[k].course_name == lista[data['students'][i]['id']][j]['course_name']:
                    initial_courses.append(list_classes[k])
        list_students.append(Student(data['students'][i]['first_name'], data['students'][i]['last_name'], initial_courses, Id=data['students'][i]['id']) )


    notfinished = True
    while notfinished:
        print("Welcome to the school system!")
        print("- 0: Exit")
        print("- 1: Create course")
        print("- 2: Create student")
        print("- 3: Add student to course")
        print("- 4: Add student's course grade")
        print("- 5: Add student's course attendance by today's date")
        print("- 6: Get student's course average")
        print("- 7: Get course's total average")
        print("- 8: Get student's total average")
        print("- 9: Get student's course attendance")
        print("- 10: Get the courses in which the student has positive average")
        print("- 11: Get course's higher score")
        print("- 12: Get course's best students")

        choice = int(input("Choose the operation you want to do from the previous list by writting the respective number."))

        if choice == 0:
            notfinished = False
        elif choice == 1:
            course = Classroom(input("Name of the course:"))
            list_classes.append(course, {}, {})
            with open('Classes.json', 'r+') as f:
                data = json.load(f)
                data['classes'].append(course.course_name)
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part
        elif choice == 2:
            name = input("First name of the student:")
            surname = input("Last name of the student:")
            student = Student(name, surname, [])
            list_students.append(student)
            with open('Student.json', 'r+') as f:
                data = json.load(f)
                data['students'].append({
                    'id': student.id,
                    'first_name': name,
                    'last_name': surname,
                    'course': [],
                })
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part

        elif choice == 3:
            std_id = int(input("Student id:"))
            course = input("Course name:")

            count = 0

            std = list(filter(lambda x: x.id == std_id , list_students))
            for i in range(len(list_students)):
                if std_id == list_students[i].id:
                    count = i
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            std[0].add_course(crs[0])
            with open('Student.json', 'r+') as f:
                data = json.load(f)
                obj = {
                    'course_name': course,
                    'grades': [],
                    'attendance': []
                }
                data['students'][count]['course'].append(obj)
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part

        elif choice == 4:
            std_id = int(input("Student id: "))
            course = input("Course name: ")
            grade = input("Grade: ")

            count = 0
            for i in range(len(list_students)):
                if std_id == list_students[i].id:
                    lista = data['students'][i]['course']
                    count = i
                    

            crs = list(filter(lambda x: x.course_name == course, list_classes))
            crs[0].add_grade(std_id, int(grade))

            count2 = 0
                
            for i in range(len(lista)):
                if course == lista[i]['course_name']:
                    count2 = i

            with open('Student.json', 'r+') as f:
                data = json.load(f)
                data['students'][count]['course'][count2]['grades'].append(int(grade))
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part

        elif choice == 5:
            std_id = int(input("Student id: "))
            course = input("Course name: ")
            date = datetime.today().strftime('%Y-%m-%d')

            crs = list(filter(lambda x: x.course_name == course, list_classes))
            crs[0].add_attendance(std_id,date)

            count = 0
            for i in range(len(list_students)):
                if std_id == list_students[i].id:
                    lista = data['students'][i]['course']
                    count = i

            count2 = 0
            for i in range(len(lista)):
                if course == lista[i]['course_name']:
                    count2 = i

            with open('Student.json', 'r+') as f:
                data = json.load(f)
                data['students'][count]['course'][count2]['attendance'].append(date)
                f.seek(0)        # <--- should reset file position to the beginning.
                json.dump(data, f, indent=4)
                f.truncate()     # remove remaining part

        elif choice == 6:
            std_id = int(input("Student id: "))
            course = input("Course name: ")
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            print("Student's course average: " + str(crs[0].get_avg_by_student(std_id)))
        elif choice == 7:
            course = input("Course name: ")
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            print("Course average: " + str(crs[0].get_total_avg()))
        elif choice == 8:
            std_id = int(input("Student id: "))
            std = list(filter(lambda x: x.id == std_id , list_students))
            print("Student's total average: " + str(std[0].get_total_avg()))
        elif choice == 9:
            std_id = int(input("Student id: "))
            course = input("Course name: ")
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            std = list(filter(lambda x: x.id == std_id , list_students))
            print("Student's attendance: " + str(crs[0].get_attendance_by_student(std_id)))
        elif choice == 10:
            std_id = int(input("Student id: "))
            std = list(filter(lambda x: x.id == std_id , list_students))
            print("Student's positive average courses" + str(std[0].get_list_positive_courses()))
        elif choice == 11:
            course = input("Course name: ")
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            print("Course's higher score: " + str(crs[0].get_higher_score()))
        elif choice == 12:
            course = input("Course name: ")
            crs = list(filter(lambda x: x.course_name == course, list_classes))
            print("Course's best student: ")
            best = crs[0].get_best_students()
            stri = ""
            if len(best) == 1:
                    stri = str(best[0])
            else:
                for i in best:
                    stri = stri + ', ' +  str(i)
            print(stri)

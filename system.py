import Student as std
class System:

    def __init__(self):
        self.students = {}

    def get_avg_by_course(self, course, student_name, student_surname):
        
        grades = std.grades[course]
        sum = 0
        
        for val in grades:
            sum += val

        return sum/len(grades)

    ##def get_total_avg(self, stu


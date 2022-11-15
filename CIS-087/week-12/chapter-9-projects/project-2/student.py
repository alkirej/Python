"""
File: student.py
Resources to manage a student's name and test scores.
"""
import random
class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverage(self):
        """Returns the average score."""
        return sum(self.scores) / len(self._scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

    def __eq__(self, other):
        """Compare student names for equality."""
        return self.getName() == other.getName()

    def __lt__(self, other):
        """Compare student names"""
        return self.getName() < other.getName()

    def __ge__(self, other):
        """Compare student names"""
        return self.getName() >= other.getName()

def begin_test(student1, op, student2):
    print( student1.getName() + op + student2.getName() + "?", end=" " )

def make_student(name,num_scores,score_val):
    student = Student(name,num_scores)
    for i in range(1,num_scores+1):
        student.setScore(i,score_val+i)
    return student

def print_list(items):
    for i in items:
        print(i)
        print()

def main():
    students = [make_student("Lara the Carrot",5,90),
                make_student("Bob the Tomato",5,95),
                make_student("Larry the Cucumber",5,60),
                make_student("Frankencelery",5,70)
               ]

    random.shuffle(students)
    print_list(students)
    print("-----------------")

    students.sort()
    print_list(students)

if __name__ == "__main__":
    main()



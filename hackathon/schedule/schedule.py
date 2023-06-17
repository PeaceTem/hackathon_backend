from .algorithm import Algorithm
from .models import Column
import random


class TimeTable():
    
    """
    This is the interface for scheduling courses
    The Algorithm class with not be interacted with in the views.py 
    """

    def __init__(self, columns):
        self.columns = columns.order_by('?')
        self.residue = []



    def __str__(self):
        return f"<TimeTable: ...>"


    def process(self):
        print(f"There are {self.columns.count()} courses.")

        #shuffling the columns before scheduling
        # random.shuffle(self.columns)

        for column in self.columns:
            print(f"Scheduling for {column} has started!")
            scheduled = Algorithm(column)._crossover()
            # check if the column has been evaluate or not so it can be added as the
            # residue part of the algorithm

            if not scheduled:
                self.residue.append(column)


        print("This are the residue of the algorithm:", self.residue)
        return True


"""
Add an health-check method to check if the timetable is conflict-free

"""






"""
Revise OOP in python:
Static Method
class method
setter and getter
polymorphism
encapsulation
abstraction

"""


def test():
    print('Testing has started!')

    cols = Column.objects.all()
    t = TimeTable(cols)
    t.process()

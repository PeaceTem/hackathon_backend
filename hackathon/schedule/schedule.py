from .algorithm import Algorithm
from .models import Column

from .modify import Modify

class TimeTable():
    
    """
    This is the interface for scheduling courses
    The Algorithm class with not be interacted with in the views.py 
    """

    def __init__(self, columns):
        # the columns are shuffled
        self.columns = columns.order_by('?')
        self.residue = []
        self.final_residue = []



    def __str__(self):
        # Use this format -> <TimeTable: Computer Science>
        return f"<TimeTable: ...>"


    def process(self):
        print(f"There are {self.columns.count()} courses.")


        for column in self.columns:
            print(f"Scheduling for {column} has started!")
            scheduled = Algorithm(column)._crossover()
            # check if the column has been evaluate or not so it can be added as the
            # residue part of the algorithm

            if not scheduled:
                self.residue.append(column)


        print("This are the residue of the algorithm:", self.residue)
        return True




    def reschedule_residue(self):
        """
        Change the venue for each course to another venue with higher capacity until the 
        course is scheduled
        """

        for r in self.residue:
            scheduled = Modify.modify_venue(r)

            if not scheduled:
                self.final_residue.append(r)



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

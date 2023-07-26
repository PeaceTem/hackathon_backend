from .algorithm import Algorithm
from .models import *

"""
All the restrictions for a department should be stored in the department model
Do the same for levels

"""

class Modify:
    
    """
    This is the class responsible for modifying a course,
    a level's time slot,
    a department's time slot
    a course's time slot and venue
    """

    def __str__(self):
        return f"<Modify: ...>"


    def process(self):
        # This method should force a course to be scheduled
        return True

    """
    Change the venue to another one with higher capacity
    """
    @classmethod
    def modify_venue(cls, column: Column, *args, **kwargs):
        for venue in Venue.objects.filter(capacity__gt=column.venue.capacity):
            done = Algorithm(column)._crossover()

            if done:
                return True

        return False



    """
    Choose a venue to take the course
    """

    @classmethod
    def assign_venue(cls,
                    column: Column,
                    venue: Venue, *args, **kwargs):
        _venue = column.venue

        if _venue != venue:
            column.venue = venue
            column.save()

        done = Algorithm(column)._crossover()

        if done:
            return True
        
        column.venue = _venue
        column.save()

        return False


    """
    The re allocate a course
    """

    @classmethod
    def course_reallocation(cls,
                            column: Column,
                            time_slot: TimeSlot,
                            row: Row, *args, **kwargs):
        """
        get the time slot and the day to be scheduled to.
        """

        if column.time_slot != time_slot:
            column.time_slot = time_slot
            column.save()
        
        cell = Cell.objects.get(row=row, column=column)
        done = Algorithm(column)._evaluate(cell)

        if not done:
            return False
        
        return True



    @classmethod
    def course_cell_exclusion(cls,
                            column: Column,
                            cell: Cell, *args, **kwargs):
        
        if cell.column != column:
            return False
        
        if cell.value == 1:
            cell.value = -1
            cell.save()

            # call the algorithm that forces a course to be scheduled
            done = Algorithm(column)._crossover()

            # change the venue if the current venue is unavailable throughout the exam period
            if not done:
                Modify.modify_venue(column)
                # the cell value should change for the new venue

            """
            Check the restrictions for the department and level
            to know whether to assign -1 to the cell value or not
            """
            # cell.value = -1
            # cell.save()


        elif cell.value == 0:
            cell.value = -1
            cell.save()

        elif cell.value -1:
            pass

        else:
            return False
        
        return True
    

    @classmethod
    def level_cells_exclusion(cls,
                            level: int,
                            time_slot: TimeSlot,
                            row: Row,
                            *args, **kwargs):
        
        courses = CourseCode.objects.filter(level=level)

        columns = Column.objects.filter(course_code__in=courses,
                                        time_slot=time_slot)
        
        for column in columns:
            cell = column.cells.get(row=row)
            Modify.course_cell_exclusion(column, cell)


        return True
    

    @classmethod
    def department_cells_exclusion(cls,
                                   department: Department,
                                   time_slot: TimeSlot,
                                   row: Row, *args, **kwargs):
        
        # use all for now
        courses = CourseCode.objects.filter(department=department)
        # print(courses)
        # courses = CourseCode.objects.all()
        columns = Column.objects.filter(course_code__in=courses,
                                        time_slot=time_slot)
        for column in columns:
            cell = column.cells.get(row=row)
            Modify.course_cell_exclusion(column, cell)

        return True



def restart(department: Department):
    courses = CourseCode.objects.filter(department=department)
    columns = Column.objects.filter(course_code__in=courses)
    for column in columns:
        for cell in column.cells.all():
            cell.value = 0
            cell.save(updated_fields=["value"])

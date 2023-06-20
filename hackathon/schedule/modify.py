from .algorithm import Algorithm
from .models import *

"""
All the restrictions for a department should be stored in the department model
Do the same for levels

"""

class Modify:
    
    """
    This is the interface for modifying a course,
    a level's time slot,
    a department's time slot

    """

    def __str__(self):
        return f"<Modify: ...>"


    def process(self):
        # This method should force a course to be scheduled
        return True



    def modify_venue(self, column: Column, *args, **kwargs):
        for venue in Venue.objects.filter(capacity__gt=column.venue.capacity):
            done = Algorithm(column)._crossover()

            if done:
                return True

        return False



    def assign_venue(self,
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


    
    def course_reallocation(self,
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



    def course_cell_exclusion(self,
                            column: Column,
                            cell: Cell, *args, **kwargs):
        if cell.column != column:
            return False
        
        if cell.value == 1:
            cell.value = -1
            cell.save()
            # call the algorithm that forces a course to be scheduled
            done = Algorithm(column)._crossover()

            if not done:
                self.modify_venue(column)
                # the cell value should change for the new venue

            """
            Check the restrictions for the department and level
            to know whether to assign -1 to the cell value or not
            """
            cell.value = 1 if True else -1
            cell.save()


        elif cell.value == 0:
            cell.value = -1
            cell.value()

        elif cell.value -1:
            pass

        else:
            return False
        
        return True
    

    
    def level_cells_exclusion(self,
                            level: int,
                            time_slot: TimeSlot,
                            row: Row,
                            *args, **kwargs):
        
        courses = CourseCode.objects.filter(level=level)

        columns = Column.objects.filter(course_code__in=courses,
                                        time_slot=time_slot)
        
        for column in columns:
            cell = column.cells.get(row=row)
            self.course_cell_exclusion(column, cell)


        return True
    

    
    def department_cells_exclusion(self,
                                   department: Department,
                                   time_slot: TimeSlot,
                                   row: Row, *args, **kwargs):
        
        
        courses = CourseCode.objects.filter(department=department)

        columns = Column.objects.filter(course_code__in=courses,
                                        time_slot=time_slot)
        
        for column in columns:
            cell = column.cells.get(row=row)
            self.course_cell_exclusion(column, cell)



        return True
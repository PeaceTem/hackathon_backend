
from .models import *


"""
Function that ensures the integrity of the data 
"""



"""
The select function returns the scheduled cell that contains a course


selection should be done by column
"""
def select(course_code, *args, **kwargs):
    course_code = CourseCode.objects.select_related('column').get(code=course_code)
    column = course_code.column
    cells = column.cells

    for cell in cells:
        if cell.value == 1:
            return cell
        
    return None


"""
The crossover function checks if a cell in the column is not scheduled
check if the venue is available on the next row

mutate will take over after the crossover has loop through all the cells in a column
"""
# check if the next cell is not -1
def crossover(cell, *args, **kwargs):
    if cell.value == 1:
        returned_cell = select(cell.column.course_code)

        # if it returns None
        if not returned_cell:
            return None

        # change the value of the current cell to 0
        # and change the value of the destination cell to 1
        elif returned_cell == cell:
            try:
                row = cell.row.get_next_by_order()
                destination_cell = Cell.objects.select_related('column', 'row').get(row=row, column=cell.column)
                cell.value = 0
                destination_cell.value = 1
                cell.save()
                destination_cell.save()
            except:
                pass
    
    return

    

"""
The evaluate function trys to assign 1 to a cell if possible
It tries to avoid re-scheduling and ensures the integrity of the algorithm


It should check the availability of the venue on the new day

"""
def evaluate(cell, *args, **kwargs):
    if cell.value == 1 or cell.value == -1:
        return
    elif cell.value == 0:
        returned_cell = select(cell.column.course_code)
        
        # if it returns None
        if not returned_cell:
            return None


        # change the value of the cell selected for evaluation to 1
        # and change the value of the cell has currently has 1 as its value to 0

        returned_cell.value = 0
        cell.value = 1

        returned_cell.save()
        cell.save()

    return
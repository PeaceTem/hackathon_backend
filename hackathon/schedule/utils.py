
from .models import *


"""
Function that ensures the integrity of the data 
"""



"""
The select function returns the scheduled cell that contains a course


selection should be done by column
"""
# def select(course_code, *args, **kwargs):
#     course_code = CourseCode.objects.select_related('column').get(code=course_code)
#     column = course_code.column
#     cells = column.cells

#     for cell in cells:
#         if cell.value == 1:
#             return cell
        
#     return None
def select(column_id, *args, **kwargs):
    column = Column.objects.prefetch_related('cells').get(id=column_id)

    for cell in column.cells.all():
        if cell.value == 1:
            return cell
    
    return Cell.objects.none()

"""
The crossover function checks if a cell in the column is not scheduled
check if the venue is available on the next row

mutate will take over after the crossover has loop through all the cells in a column
"""
# check if the next cell is not -1
def crossover(column_id, *args, **kwargs):
    returned_cell = select(column_id)

    # if it returns None
    if not returned_cell:
        return None

    # change the value of the current cell to 0
    # and change the value of the destination cell to 1
    else:
        # row = returned_cell.row.get_next_by_order()
        row = Row.objects.filter(id__gt=returned_cell.row.id).order_by('id').first()
        destination_cell = Cell.objects.select_related('column', 'row').get(row=row, column=returned_cell.column)
        print("first stage")
        # checking if the next cell value is not -1
        if destination_cell.value != -1:
            venue = returned_cell.column.venue
            venue_columns  = venue.columns.select_related('time_slot').exclude(id=returned_cell.column.id)
            A = returned_cell.column.time_slot.start_hour
            B = returned_cell.column.time_slot.end_hour
            for vc in venue_columns:
                C = vc.time_slot.start_hour
                D = vc.time_slot.end_hour

                # the execution terminates if the time clashes
                if ((A<=C<B) or (A<D<=B) or (C<=A<D) or (C<B<=D)):
                    print('The time clashes')
                    print(vc)
                    return 
                

            print('The time does not clash')
            returned_cell.value = 0
            destination_cell.value = 1
            returned_cell.save()
            destination_cell.save()
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
        returned_cell = select(cell.column.id)
        
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



def test():
    column = Column.objects.first()
    crossover(column.id)
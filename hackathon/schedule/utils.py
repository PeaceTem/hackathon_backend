
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
def select(column_id: int, *args, **kwargs):
    column = Column.objects.prefetch_related('cells').get(id=column_id)

    for cell in column.cells.all():
        if cell.value == 1:
            return cell
    
    return Cell.objects.none()



def check_availability():
    pass
"""
The crossover function checks if a cell in the column is not scheduled
check if the venue is available on the next row

mutate will take over after the crossover has loop through all the cells in a column
"""
# check if the next cell is not -1
def crossover(column_id: int, *args, **kwargs):
    returned_cell = select(column_id)

    # if it returns None
    if not returned_cell:
        return None

    # change the value of the current cell to 0
    # and change the value of the destination cell to 1
    # check for any clashing venue
    # row = returned_cell.row.get_next_by_order()

    

    if returned_cell.row == Row.objects.last():
        row = Row.objects.first()
    else:
        row = Row.objects.filter(id__gt=returned_cell.row.id).order_by('id').first()

    destination_cell = Cell.objects.select_related('column', 'row').get(row=row, column=returned_cell.column)

    while destination_cell.value == -1:
        row = row + 1
        destination_cell = Cell.objects.select_related('column', 'row').get(row=row, column=returned_cell.column)

    print("first stage")
    # checking if the next cell value is not -1
    if destination_cell.value != -1:
        venue = destination_cell.column.venue
        venue_columns  = venue.columns.select_related('time_slot').exclude(id=returned_cell.column.id)
        A = destination_cell.column.time_slot.start_hour
        B = destination_cell.column.time_slot.end_hour
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
def evaluate(cell: Cell, *args, **kwargs):
    if cell.value == 1 or cell.value == -1:
        output = 'The cell is already taken' if cell.value == 1 else 'The cell cannot be taken'
        print(output)
        return
    elif cell.value == 0:
        returned_cell = select(cell.column.id)
        
        # if it returns None
        if not returned_cell:
            return None


        # change the value of the cell selected for evaluation to 1
        # and change the value of the cell has currently has 1 as its value to 0

        venue = cell.column.venue
        venue_columns  = venue.columns.select_related('time_slot').exclude(id=returned_cell.column.id)
        A = cell.column.time_slot.start_hour
        B = cell.column.time_slot.end_hour
        for vc in venue_columns:
            C = vc.time_slot.start_hour
            D = vc.time_slot.end_hour

            # the execution terminates if the time clashes
            if ((A<=C<B) or (A<D<=B) or (C<=A<D) or (C<B<=D)):
                print('The time clashes')
                print(vc)

                return False
            

        print('The time does not clash')
        returned_cell.value = 0
        cell.value = 1
        returned_cell.save()
        cell.save()


    return True



def test():
    column = Column.objects.first()
    crossover(column.id)



def test2():
    # cell = Cell.objects.get(id=29)
    column = Column.objects.get(course_code__code='E')
    row = Row.objects.get(day__day='Thursday')
    cell = Cell.objects.get(column=column, row=row)
    evaluate(cell)


def test3():
    time_slot = TimeSlot.objects.get(id=9)
    column = Column.objects.get(id=8)
    print(column.__mutate__(time_slot=time_slot))

    
def test4():
    column = Column.objects.get(course_code__code='E')
    crossover(column.id)   

import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa


# turn and html page to pdf
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
     if not pdf.err:
          return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path


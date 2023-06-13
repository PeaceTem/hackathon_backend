"""
This file contains the main algorithm to generate the timetable
"""



"""
Apply for abroad remote jobs

"""
from .models import *
from django.core.exceptions import EmptyResultSet
import random,math


class Algorithm():
    """
    Add the all the time_slots to a class variable cls.time_slots
    and use random on it instead of adding a delimiter to the class
    
    
    """

    time_slots = TimeSlot.objects.all()


    def __init__(self, column: Column):
        self.column = column
        self.crossover_number_of_steps = 0
        self.crossover_delimiter = 0
        self.time_slot_delimiter = 0
        self.venue_delimiter = 0


    def __str__(self):
        return f"<Algorithm: {self.column}>"


    def mutation(self, *args, **kwargs):
        time_slot = None
        venue = None
        try:
            if not kwargs['time_slot'] == None:
                time_slot = kwargs['time_slot']
        except KeyError:
            pass

        try:
            if not kwargs['venue'] == None:
                venue = kwargs['venue']
        except KeyError:
            pass

        
        if venue:
            self.column.venue = venue

        if time_slot:
            self.column.time_slot = time_slot
        
        self.column.save()

        return True


    def selection(self, *args, **kwargs):
        column = Column.objects.prefetch_related('cells').get(id=self.column.id)

        for cell in column.cells.all():
            if cell.value == 1:
                return cell
        
        return None


    def selection_service(self, column, *args, **kwargs):
        column = Column.objects.prefetch_related('cells').get(id=column.id)

        for cell in column.cells.all():
            if cell.value == 1:
                return cell
        print(f"{column} is returning a None value")
        return None


    def _crossover(self, *args, **kwargs):
        """
        Get all the cells in a column
        filter out the cells that doesn't have 0 as their value
        select a random cell
        start the crossover for the cell

        """

        cells = self.column.cells.exclude(value=-1)
        # clean the column before scheduling 

        for cell in cells:
            if cell.value == 1:
                cell.value = 0
                cell.save()


        evaluated = False
        # set the first TimeSlot
        self.time_slot_delimiter = TimeSlot.objects.count() - 1
        while not evaluated:

            while not evaluated and cells.count() > 0:
                print("Taking a new cell out of the column")
                cell = cells[math.floor(random.random()*cells.count())]
                
                # this block of code doesn't need because the cells values are now 0
                """
                if cell.value == 1:
                    evaluated = True
                """

                # check if the cell is available for scheduling
                evaluated = self._evaluation(cell)
                
                if not evaluated:
                    # remove the cell if it is not available
                    print("Going to another cell")
                    cells = cells.exclude(id=cell.id)

            
            if not evaluated and self.time_slot_delimiter <= 0:
                print('The time slot has been exhausted!')

                return False


            elif not evaluated:
                _time_slot = self.column.time_slot + 1
                print(f'Time slot changed successfully from {self.column.time_slot} to {_time_slot}')

                self.mutation(time_slot=_time_slot)
                # make sure this function take in all the TimeSlots
                self.time_slot_delimiter -= 1

        print(f'successfully scheduled {self.column} for {cell.row}')
        print()
        print()

        return True





    def _evaluation(self, cell: Cell, *args, **kwargs):
        """
        You can store other venues in a global variable later
        

        use day to check also

        turn all these small block of code to a method in this class
        """

        # change the value of the cell selected for evaluation to 1
        # and change the value of the cell has currently has 1 as its value to 0

        venue = self.column.venue
        venue_columns  = venue.columns.select_related('time_slot').prefetch_related('cells').exclude(id=self.column.id)
        A = self.column.time_slot.start_hour
        B = self.column.time_slot.end_hour
        for vc in venue_columns:
            # print(f"{self.column} is checking a new column: {vc}")
            returned_cell = self.selection_service(vc) # allow select_related('row') in the returned_cell

            if returned_cell is not None:
                if cell.row == returned_cell.row:
                    print(f"The day clashes for {cell} and {returned_cell}")
                    C = vc.time_slot.start_hour
                    D = vc.time_slot.end_hour

                    # the execution terminates if the time clashes
                    if ((A<=C<B) or (A<D<=B) or (C<=A<D) or (C<B<=D)):
                        print(f'The time clashes between {vc} and {self.column}')
                        # print(vc)

                        return False



        print('The time does not clash')

        cell.value = 1
        cell.save()
        print(f"{self.column} has been evaluated")



        return True



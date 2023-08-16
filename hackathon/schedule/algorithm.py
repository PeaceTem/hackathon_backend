"""
This file contains the main algorithm to generate the timetable

There are 3 different timeslots: 8-11, 12-3, 3:30-6:30.
The admin can add as many rows(days) as he/she likes.
Each column consists of a course, a timeslot and a venue. The venue is given to the column based on
"""

from .models import *
from django.core.exceptions import EmptyResultSet
import random, math


class Algorithm:
    # the list of all the timeslots available
    # I haven't implement this
    time_slots = TimeSlot.objects.all()


    def __init__(self, column: Column):
        self.column = column
        self.crossover_number_of_steps = 0
        self.crossover_delimiter = 0
        self.time_slot_delimiter = 0
        self.venue_delimiter = 0


    def __str__(self):
        return f"<Algorithm: {self.column}>"

    # "The time slots and the venue can be changed here"
    #
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

    # We want to check if the column has being scheduled, then return the cell
    def selection(self, *args, **kwargs):
        column = Column.objects.prefetch_related('cells').get(id=self.column.id)

        for cell in column.cells.all():
            if cell.value == 1:
                return cell
        
        # it'll return None if the course has not been scheduled
        return None

    # We want to check if another column has being scheduled, then return the cell
    def selection_service(self, column: Column, *args, **kwargs):
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
        
        # clean the column before scheduling, i.e. remove the schedule
        for cell in cells:
            if cell.value == 1:
                cell.value = 0
                cell.save()

        # this means the course has not been scheduled
        evaluated = False
        # set the first TimeSlot
        self.time_slot_delimiter = TimeSlot.objects.count() - 1
        while not evaluated:

            while not evaluated and cells.count() > 0:
                print("Taking a new cell out of the column")
                cell = cells[math.floor(random.random()*cells.count())]
                
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




    # This is the main method that does the magic
    def _evaluation(self, cell: Cell, *args, **kwargs):
        """
        Do this later
        Check if the course is not clashing with any university course
        then check if it is not clashing with any faculty course

        The departmental courses check has been done.

        """




        """
        This method tries to schedule a course
        It checks all the courses that share the same venue with the course for any clashes
        by checking if the day clashes, then if the timeslot clashes
        """

        venue = self.column.venue
        venue_columns  = venue.columns.select_related('time_slot').prefetch_related('cells').exclude(id=self.column.id)
        A = self.column.time_slot.start_hour
        B = A + 3 #self.column.time_slot.end_hour
        for venue_column in venue_columns:
            # print(f"{self.column} is checking a new column: {venue_column}")
            returned_cell = self.selection_service(venue_column) # allow select_related('row') in the returned_cell

            if returned_cell is not None:
                # checking if the day clashes
                if cell.row == returned_cell.row:
                    print(f"The day clashes for {cell} and {returned_cell}")
                    C = venue_column.time_slot.start_hour
                    D = C + 3 #venue_column.time_slot.end_hour

                    # the execution terminates if the time clashes
                    if ((A<=C<B) or (A<D<=B) or (C<=A<D) or (C<B<=D)):
                        print(f'The time clashes between {venue_column} and {self.column}')
                        # print(venue_column)

                        return False
    

        print('The time does not clash')

        cell.value = 1
        cell.save()
        print(f"{self.column} has been evaluated")



        return True



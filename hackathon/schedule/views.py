from django.shortcuts import render
from .models import *
# Create your views here



class Schedule():

    def sort_activities(self, columns):
        columns = sorted(columns, key=sortQuiz)
        i = 0
        venue_schedule = []
        # print(columns[i])
        venue_schedule.append(columns[i])
        for j in range(1, len(columns)):
            if columns[j].time_slot.start_hour >= columns[i].time_slot.end_hour:
                venue_schedule.append(columns[j])
                # print(columns[j])
                i = j

        return venue_schedule
        

def sortQuiz(e):
    return e.time_slot.start_hour


def testing(request):
    s = Schedule()
    columns = Column.objects.select_related("time_slot", "venue").all()
    
    #sort columns based on venues
    venues_sorted_columns = []
    venues = []
    for column in columns:
        if column.venue not in venues:
            venues.append(column.venue)
            venues_sorted_columns.append([column])
        else:
            index = venues.index(column.venue)
            venues_sorted_columns[index].append(column)

    # print(venues_sorted_columns)
    # print()

    for column in venues_sorted_columns:
        # print(column)
        print(s.sort_activities(column))
        print()




    return render(request, 'schedule/testing.html')
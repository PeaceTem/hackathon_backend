from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.http import JsonResponse

from .models import *

from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View

from django.contrib.auth.views import LoginView
from .forms import CustomUserForm, PasswordForm
from django.contrib.auth import login, authenticate, update_session_auth_hash

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import gettext_lazy as _
# Create your views here.
from .utils import evaluate, crossover, select

from .schedule import TimeTable

from .modify  import Modify



class Schedule():

    def sort_activities(self, columns):
        # sort the columns in the order of the start_hour
        columns = sorted(columns, key=sortKey)
        columns.sort(key=sortKey)
        i = 0
        venue_schedule = []
        # the first column is been picked
        venue_schedule.append(columns[i])
        for j in range(1, len(columns)):
            if columns[j].time_slot.start_hour >= columns[i].time_slot.end_hour:
                venue_schedule.append(columns[j])
                # print(columns[j])
                i = j

        return venue_schedule
        

def sortKey(e):
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

    print(venues_sorted_columns)
    # print()

    for column in venues_sorted_columns:
        print(column)
        # print(s.sort_activities(column))
        print()

    """
    add the s.sort_activites function to the stuff
    """


    day = Day.objects.first()
    cells = Cell.objects.all()
    print(day)
    # print(venues_sorted_columns)

    vet = []
    for v in venues_sorted_columns:
        for a in v:
            vet.append(a)
    print(vet)



    for cell in cells:
        if cell.row.day == day and cell.column in vet:
            print(cell)
            evaluate(cell)
            # cell.value = 1
            cell.save()

    venues_sorted_columns = zip(venues, venues_sorted_columns)
    context = {
            "venues": venues,
            "venues_sorted_columns": venues_sorted_columns ,   
        }

    return render(request, 'schedule/testing.html', context)







class CreateSuperUser(FormView):
    template_name = 'schedule/registration.html'
    form_class = CustomUserForm
    redirect_authenticated_user = True
    success_url = HttpResponseRedirect("/admin")
    
        
    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        email = self.request.POST.get('email')

        User.objects.create_superuser(username=username, password=password, email=email)
        print("It works")
        user = authenticate(self.request, username=username, password=password)
        messages.success(self.request, f"You are logged in as {username}")
        login(self.request, user)
        print("It works 2")
        return HttpResponsePermanentRedirect("/admin/")
        return super(CreateSuperUser, self).post(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.success(self.request, f"{self.request.user}, you've already registered!")
            return HttpResponsePermanentRedirect('/admin/')
        
        return super(CreateSuperUser, self).get(request, *args, **kwargs)


class TimeMatrix(LoginRequiredMixin, TemplateView):
    template_name = 'schedule/time_matrix.html'

    def post(self, request, *args, **kwargs):
        TimeTable(Column.objects.prefetch_related('cells').select_related('course_code', 'venue', 'time_slot').all()).process()
        return redirect('schedule-courses')
        # return super(TimeMatrix, self).get(request, *args, **kwargs)
    



    # get all the data that will be rendered to the user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = Column.objects.select_related('time_slot').all()
        rows = Row.objects.select_related('day').all()
        cells = Cell.objects.select_related('column', 'row').all()
        days = Day.objects.all()
        time_slots = TimeSlot.objects.all()


        context['columns'] = columns
        context['rows'] = rows
        context['cells'] = cells
        context['days'] = days
        context['time_slots'] = time_slots

        return context



class VenueTimetable(TemplateView):
    template_name = 'schedule/venue_timetable.html'


    def get(self, request, venue, *args, **kwargs):

        self.venue = venue
        return super(VenueTimetable, self).get(request, venue, *args, **kwargs)



    def get_context_data(self, **kwargs):
        print(self.venue)
        context = super().get_context_data(**kwargs)
        venue = Venue.objects.get(name=self.venue)
        columns = Column.objects.select_related('time_slot').prefetch_related('cells').filter(venue=venue)
        cells = Cell.objects.none()
        for column in columns:
            k = column.cells.select_related('column', 'row').all()
            cells = cells.union(k)
        days = Day.objects.all()
        time_slots = TimeSlot.objects.all()

        print(cells)
        context['venue'] = venue
        context['columns'] = columns
        context['cells'] = cells
        context['days'] = days
        context['time_slots'] = time_slots


        return context





from .utils import render_to_pdf
class GeneratePDF(View):
    # time matrix
    def get(self, request, *args, **kwargs):
        # template = get_template('quiz/takequiz.html')

        columns = Column.objects.select_related('time_slot').all()
        rows = Row.objects.select_related('day').all()
        cells = Cell.objects.select_related('column', 'row').all()
        days = Day.objects.all()
        time_slots = TimeSlot.objects.all()

        context = {
            'columns': columns,
            'rows': rows,
            'cells': cells,
            'days': days,
            'time_slots' : time_slots,
        }

        pdf = render_to_pdf('schedule/pdf.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"Matrix.pdf"
            content = f"inline; filename={filename}"
            # content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content

            return response
        return HttpResponse("Not Found!")



"""
This view should be called at the response to a button(schedule)

"""


class ScheduleCourses(TemplateView):
    template_name = 'schedule/timetable.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = Column.objects.select_related('time_slot').all()
        rows = Row.objects.select_related('day').all()
        cells = Cell.objects.select_related('column', 'row').all()
        days = Day.objects.all()
        # change the time slot
        time_slots = TimeSlot.objects.all()
        context['columns'] = columns
        context['rows'] = rows
        context['cells'] = cells
        context['days'] = days
        context['time_slots'] = time_slots

        return context




class DepartmentExclusion(View):

    def get(self, request):
        category = self.request.GET.get('category')

        # return all the available levels for the department
        if category == "level":
            return JsonResponse({'level': [100, 200, 300, 400, 500]})
        

        
        elif category == "course":
            # use serializers later
            courses = CourseCode.objects.all()
            return JsonResponse({'courses' : [*courses]})

        elif category == 'all':
            pass

        return JsonResponse({'modified': True})

    def post(self, request):
        category = self.request.POST.get('category')
        time_slot = self.request.POST.get('time_slot')

        time_slot = TimeSlot.objects.get(id=int(time_slot))

        row = self.request.POST.get('row')

        row = Row.objects.get(id=int(row))

        print("started departmental cells exclusion")

        if category == "level":

            level = int(self.request.POST.get('level'))
            Modify.level_cells_exclusion(level, time_slot, row)

        elif category == "course":
            pass

        elif category == "all":
            # exclude a time slot / row for the whole department
            department = Department.objects.get(name='Computer Science')
            Modify.department_cells_exclusion(department, time_slot, row)
            print("finished departmental cells exclusion")

        return JsonResponse({'modified': True})



from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect
from .models import *

from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView



from django.contrib.auth.views import LoginView
from .forms import CustomUserForm, PasswordForm
from django.contrib.auth import login, authenticate, update_session_auth_hash

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.translation import gettext_lazy as _
# Create your views here.
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


    cell = Cell.objects.first()
    cell.__mutate__()
    # mutate(cell)

    return render(request, 'schedule/testing.html')




class CreateSuperUser(FormView):
    template_name = 'schedule/registration.html'
    form_class = CustomUserForm
    redirect_authenticated_user = True
    success_url = HttpResponseRedirect("/admin")
    
        
    def post(self, request, *args, **kwargs):
        # form.save()
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


class TimeMatrix(TemplateView):
    template_name = 'schedule/time_matrix.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        columns = Column.objects.all()
        rows = Row.objects.all()
        cells = Cell.objects.all()
        days = Day.objects.all()
        time = [0,1,2,3,4,5,6,7,8,9,10]
        context['columns'] = columns
        context['rows'] = rows
        context['cells'] = cells
        context['days'] = days
        context['time'] = time

        return context

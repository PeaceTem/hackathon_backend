from django.db import models
from department.models import Department

# Create your models here.


class CourseCode(models.Model):
    LEVELS = (
        (100, 100),
        (200, 200),
        (300, 300),
        (400, 400),
        (500, 500),

    )
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    student_population = models.PositiveSmallIntegerField(default=1)
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="courses")


    def __str__(self):
        return f"{self.code}"


class Venue(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="venues")


    def __str__(self):
        return f"{self.name}"




#format this later using the techniques learnt in csc231 :2d
class TimeSlot(models.Model):
    HOURS = (
        zip(range(0,24), range(0,24))
    )


    HOURS2 = (
        zip(range(0,24), range(0,24))
    )


    MINUTES = (zip(range(0,60), range(0,60)))

    MINUTES2 = (zip(range(0,60), range(0,60)))



    start_hour = models.PositiveSmallIntegerField(choices=HOURS, default=0)
    start_minute = models.PositiveSmallIntegerField(choices=MINUTES, default=0)

    end_hour = models.PositiveSmallIntegerField(choices=HOURS2, default=0)
    end_minute = models.PositiveSmallIntegerField(choices=MINUTES2, default=0)

    @property
    def start_time(self):
        return f"{self.start_hour:02d}:{self.start_minute:02d}"

    @property
    def end_time(self):
        return f"{self.end_hour:02d}:{self.end_minute:02d}"

    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    
    # recursive algorithm combined with backtracking algorithm
    def __add__(self, value=1):
        if value == 0:
            return self
        
        
        if self == TimeSlot.objects.last():
            return TimeSlot.objects.first() + (value - 1)
            
        else:
            return TimeSlot.objects.filter(id__gt=self.id).order_by('id').first() + (value - 1)











class Day(models.Model):
    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday")
    )

    WEEKS = (
        ("one", "one"),
        ("two", "two"),
        ("three", "three")
    )
    day = models.CharField(max_length=50, choices=DAYS)
    week = models.CharField(max_length=50, choices=WEEKS)



    def __str__(self):
        return f"week {self.week}, {self.day}"




class Supervisor(models.Model):
    name = models.CharField(max_length=100)
    course = models.OneToOneField(CourseCode, null=True, blank=True, on_delete=models.CASCADE, related_name='supervisor')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="supervisors")


    def __str__(self):
        return f"{self.name}"




# The classes for the relations
"""
Add constraints to the model

two columns cannot have the same course

"""
class Column(models.Model):
    course_code = models.OneToOneField(CourseCode, on_delete=models.CASCADE, related_name="column")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="columns")
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.CASCADE, related_name="columns")

    def __str__(self):
        return f"{self.course_code}, {self.time_slot}, {self.venue}"


    def __mutate__(self, *args, **kwargs):
        print('The mutation works!')
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
            self.venue = venue

        if time_slot:
            self.time_slot = time_slot
        
        self.save()

        return self




    def create(self, **obj):
        venues = Venue.objects.order_by("capacity")
        for v in venues:
            if obj['course_code'].student_population <= v.capacity:
                obj['venue'] = v
                break

        return super().create(self, **obj)


    def save(self, *args, **kwargs):
        venues = Venue.objects.order_by("capacity")
        for v in venues:
            if self.course_code.student_population <= v.capacity:
                self.venue = v
                break

        return super().save(*args, **kwargs)
        

"""
Add constraints to the model

two rows cannot have the same date

"""
class Row(models.Model):
    day = models.OneToOneField(Day, on_delete=models.CASCADE, related_name="row")


    def __str__(self):
        return f"{self.day}"

    # recursive algorithm (later) combined with backtracking algorithm
    def __add__(self, value=1):
        if value == 0:
            return self
        
        
        if self == Row.objects.last():
            return Row.objects.first() + (value - 1)
        else:
            # row = Row.objects.filter(id__gt=self.id).order_by('id')[value-1:value][0]
            return Row.objects.filter(id__gt=self.id).order_by('id')[0] + (value - 1)


        

class Cell(models.Model):
    VALUES = (zip(range(-1,2) , range(-1,2)))
    
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cells")
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="cells")
    value = models.SmallIntegerField(choices=VALUES, default=0)
    
    def __str__(self):
        return f"{self.column.course_code}({self.column.venue})"
    

from django.db import models


# Create your models here.


class CourseCode(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    student_population = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return f"{self.code}"



class Venue(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(default=1)
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
        return f"{self.day}"




class Supervisor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"




# The classes for the relations

class Column(models.Model):
    course_code = models.OneToOneField(CourseCode, on_delete=models.CASCADE, related_name="column")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="column")
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.CASCADE, related_name="column")


    def __str__(self):
        return f"{self.course_code}, {self.time_slot}, {self.venue}"


    def __mutate__(self, *args, **kwargs):
        print('The mutation works!')
        timeslot = None
        try:
            if not kwargs['timeslot'] == None:
                timeslot = kwargs['timeslot']
        except KeyError:
            pass

        try:
            if not kwargs['venue'] == None:
                venue = kwargs['venue']
        except KeyError:
            pass

        if venue:
            self.venue = venue

        if timeslot:
            self.time_slot = timeslot
        

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
        


class Row(models.Model):
    day = models.OneToOneField(Day, on_delete=models.CASCADE, related_name="row")


    def __str__(self):
        return f"{self.day}"


    

    # def __crossover__(self):
    #     next_object = self.get_next_by_order()
        

class Cell(models.Model):
    VALUES = (zip(range(-1,2) , range(-1,2)))
    
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cell")
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="cell")
    value = models.SmallIntegerField(choices=VALUES, default=0)
    # i = models.PositiveSmallIntegerField()
    # j = models.PositiveSmallIntegerField()
    # def __str__(self):
    #     return f"({self.row}, {self.column})"
    
    def __str__(self):
        return f"{self.column.course_code}, {self.column.venue}"
    

    def __select__(self):
        print('The selection works')
        return 1


# Create Pastor Adeshida PowerPoint Presentation
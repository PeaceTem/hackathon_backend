from django.db import models

# Create your models here.


class CourseCode(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.code}"


class Venue(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

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
        return f"{self.start_hour}:{self.start_minute}"

    @property
    def end_time(self):
        return f"{self.end_hour}:{self.end_minute}"

    
    
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
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name="column")
    venue = models.OneToOneField(Venue, on_delete=models.CASCADE, related_name="column")


    def __str__(self):
        return f"{self.course_code}, {self.time_slot}, {self.venue}"



class Row(models.Model):
    day = models.OneToOneField(Day, on_delete=models.CASCADE, related_name="row")


    def __str__(self):
        return f"{self.day}"




class Cell(models.Model):
    VALUES = (zip(-1,2), zip(-1,2))
    
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cell")
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="cell")
    value = models.SmallIntegerField(choices=VALUES)

    def __str__(self):
        return f"({self.row}, {self.column})"
    






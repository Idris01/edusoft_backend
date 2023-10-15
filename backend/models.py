from django_countries.fields import CountryField
from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class University(BaseModel):
    website = models.URLField(null=False, blank=False)
    history = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=50, null=False)
    postal_code = models.CharField(max_length=15, null=False, blank=False)
    accomodation = models.TextField(help_text="details of accomodation")


    language = models.CharField(max_length=15, default='English', null=False)

    def __str__(self):
        return self.name

class Department(BaseModel):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    about = models.TextField(help_text="brief information about the department/school")
    
    def __str__(self):
        return f"{self.name} in {self.university.name}"

class Course(BaseModel):
    department = models.ForeignKey(Department, null=False, on_delete=models.CASCADE)
    about = models.TextField(help_text="course description")

    def __str__(self):
        return "{} in {}".format(
                self.department,
                self.department.univerity)

class Tuition(BaseModel):
    degree = models.ForeignKey('Degree', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, help_text="tuition fee in dollars ($)")
    detail = models.TextField(help_text="details info about the tuition fee")

    def __str__(self):
        return "${} for {} in {}".format(
                self.amount, self.degree.name,
                self.course.name)


class Degree(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    about = models.TextField(help_text="breif details about degree")

    def __str__(self):
        return self.name

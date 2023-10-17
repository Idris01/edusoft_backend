from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


FULFILLED = "Fullfilled"
INITIATED = "Initiated"
PROCESSING = "Processing"

CONS_CHOICES = (
    ("Initialized", INITIATED),
    ("Proceasing", PROCESSING),
    ("fullfilled", FULFILLED),
)


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, null=False, help_text="name or title", blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AppUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    UNIQUE_TOGETHER = ("email", "username")
    REQUIRED_FIELDS = ("password", "username", "first_name", "last_name")


class Consultation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=CONS_CHOICES)

    def __str__(self):
        return "{} by {} with satatus{}".format(self.name, self.user.username, self.status)


class FeedBack(BaseModel):
    rating = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5)),
        help_text="""level of satisafaction
             from 1 to 5, 1 being the leas
             satisfaction""",
    )
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)

    def __str__(self):
        return "{} Rating by {}".format(self.rating, self.consultation)


class University(BaseModel):
    website = models.URLField(null=False, blank=False)
    history = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=50, null=False)
    postal_code = models.CharField(max_length=15, null=False, blank=False)
    accomodation = models.TextField(help_text="details of accomodation")

    language = models.CharField(max_length=15, default="English", null=False)

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
        return "{} in {}".format(self.department, self.department.univerity)


class Tuition(BaseModel):
    degree = models.ForeignKey("Degree", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text="tuition fee in dollars ($)"
    )
    detail = models.TextField(help_text="details info about the tuition fee")

    def __str__(self):
        return "${} for {} in {}".format(self.amount, self.degree.name, self.course.name)


class Degree(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    about = models.TextField(help_text="breif details about degree")

    def __str__(self):
        return self.name


class Officer(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, blank=False, null=False)
    portfolio = models.CharField(
        max_length=150, help_text="Brief Educational Portfolio", blank=False
    )

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Length
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


models.CharField.register_lookup(Length)

# define consultation status constants
FULFILLED = "Fullfilled"
INITIATED = "Initiated"
PROCESSING = "Processing"

# define consultation status choice fields
CONS_CHOICES = (
    ("Initiated", INITIATED),
    ("Processing", PROCESSING),
    ("Fullfilled", FULFILLED),
)


# token type constants
RESET = "reset"
ACTIVATE = "activate"

# define token type fields
TOKEN_CHOICES = (
    ("reset", RESET),
    ("activate", ACTIVATE),
)

# define payment status constants
PENDING = "pending"
SUCCESS = "success"
FAILED = "failed"
PROCESSING = "processing"

# define payment status choice fields
PAYMENT_STATUS = (
    ("Success", SUCCESS),
    ("Pending", PENDING),
    ("Failed", FAILED),
    ("Processing", PROCESSING),
)

# gender options constants
MALE = "male"
FEMALE = "female"

# define gender options choice fields
GENDERS = (
    ("male", MALE),
    ("female", FEMALE),
)


class BaseModel(models.Model):
    """An abstract class the define related fieldsfor various models

    id (uuid): unique identification for the model
    name (string): name of the respective item
    created_at (datetime): date and time of object creation
    updated_at (datetime): last uodated date and time
    """


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, null=False, help_text="name or title", blank=False, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("name",)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_not_empty",
                check=models.Q(name__length__gt=0),
            )
        ]


class BaseModelNameNoUnique(models.Model):
    """ Also a base model but without name field set as uniqie"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, null=False, help_text="name or title", blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("name",)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_not_empty",
                check=models.Q(name__length__gt=0),
            )
        ]


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        help_text="user profile",
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=150, blank=False)
    nationality = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, null=True
    )
    gender = models.CharField(choices=GENDERS, max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class AppUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    UNIQUE_TOGETHER = ("email", "username")
    REQUIRED_FIELDS = ("password", "username", "first_name", "last_name")


class ActivationToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False
    )
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=10, choices=TOKEN_CHOICES, default=ACTIVATE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)


class Consultation(BaseModelNameNoUnique):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=CONS_CHOICES)
    message = models.CharField(max_length=150, help_text="Anything you want us to know")
    sheduled_date = models.DateTimeField()

    def __str__(self):
        return "{} by {} with satatus{}".format(self.name, self.user.username, self.status)


class Payment(BaseModelNameNoUnique):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)


class FeedBack(BaseModelNameNoUnique):
    rating = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(5)),
        help_text="""level of satisafaction
             from 1 to 5, 1 being the least
             satisfaction""",
    )
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)

    def __str__(self):
        return "{} Rating by {}".format(self.rating, self.consultation)


class Language(BaseModel):
    """define Language model"""

    def __str__(self):
        return self.name


class University(BaseModel):
    website = models.URLField(null=False, blank=False)
    history = models.TextField(help_text="brief history of university")
    country = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, blank=True, null=True
    )
    city = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, blank=True, null=True
    )
    postal_code = models.CharField(max_length=15, null=False, blank=False)
    accomodation = models.TextField(help_text="details of accomodation")

    languages = models.ManyToManyField(Language, blank=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="universities",
    )

    def __str__(self):
        return self.name


class Department(BaseModelNameNoUnique):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    about = models.TextField(help_text="brief information about the department/school")

    class Meta:
        unique_together = ["name", "university"]

    def __str__(self):
        return f"{self.name} in {self.university.name}"


class Course(BaseModelNameNoUnique):
    department = models.ForeignKey(Department, null=False, on_delete=models.CASCADE)
    about = models.TextField(help_text="course description")

    class Meta:
        unique_together = ["name", "department"]
        ordering = ("name",)

    def __str__(self):
        return "{} in {}".format(self.name, self.department.university)


class Tuition(BaseModelNameNoUnique):
    degrees = models.ManyToManyField("Degree", blank=True)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text="tuition fee in dollars ($)"
    )
    detail = models.TextField(help_text="details info about the tuition fee")

    def __str__(self):
        return "$Tution: {}".format(self.amount)


class Degree(BaseModelNameNoUnique):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="degrees")
    about = models.TextField(help_text="breif details about degree")

    class Meta:
        unique_together = ["name", "course"]

    def __str__(self):
        return f"{self.name}: {self.course}"


class Officer(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, blank=False, null=False)
    portfolio = models.CharField(
        max_length=150, help_text="Brief Educational Portfolio", blank=False
    )

    def __str__(self):
        return self.name

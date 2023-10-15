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

    language = models.CharField(max_length=15, default='English', null=False)

    def __str__(self):
        return self.name

class Course(BaseModel):
    university_id = models.ForeignKey(University, null=False, on_delete=models.CASCADE)
    degree = models.ForeignKey('Degree', blank=False, on_delete=models.CASCADE)

class Degree(BaseModel):
    pass

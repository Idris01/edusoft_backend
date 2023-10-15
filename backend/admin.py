from django.contrib import admin
from .models import University, Degree, Course

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CouseAdmin(admin.ModelAdmin):
    pass

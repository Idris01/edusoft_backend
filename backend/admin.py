from django.contrib import admin
from .models import (
    University,
    Degree,
    Course,
    Department,
    Tuition,
    Officer,
    FeedBack,
    Consultation,
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    pass


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    pass


@admin.register(Tuition)
class TuitionAdmin(admin.ModelAdmin):
    pass

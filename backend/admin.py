from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cities_light.admin import City, Country, Region, SubRegion
from .models import (
    AppUser,
    University,
    Degree,
    Course,
    Department,
    Tuition,
    Officer,
    FeedBack,
    Consultation,
    Payment,
    Language,
)

admin.site.unregister(City)
admin.site.unregister(Country)
admin.site.unregister(Region)
admin.site.unregister(SubRegion)


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    pass


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """Update some required  attributes"""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

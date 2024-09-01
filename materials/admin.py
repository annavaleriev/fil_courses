from django.contrib import admin

from materials.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["title"]

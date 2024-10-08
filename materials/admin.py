from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["title"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["title"]

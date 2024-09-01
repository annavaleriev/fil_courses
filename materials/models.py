from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Модель для курсов"""

    title = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        verbose_name="Описание курса", **NULLABLE, help_text="Введите описание курса"
    )
    preview = models.ImageField(
        upload_to="course/",
        verbose_name="Превью курса",
        **NULLABLE,
        help_text="Загрузите превью курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return f"Курс {self.title}"


class Lesson(models.Model):
    """Модель для уроков"""

    title = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", **NULLABLE, help_text="Введите описание урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lessons",
        help_text="Выберите курс",
    )
    preview = (
        models.ImageField(
            upload_to="lesson/",
            verbose_name="Превью урока",
            **NULLABLE,
            help_text="Загрузите превью урока",
        ),
    )
    video = models.URLField(
        verbose_name="Видео урока", help_text="Введите ссылку на видео урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return f"Урок {self.title} из курса {self.course.title}"

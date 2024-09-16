from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей тестовых
        self.admin_user = User.objects.create_superuser(username="admin", email="admin@admin.com", password="admin")
        self.moder_user = User.objects.create_user(username="moder", email="moder@moder.com", password="moder")
        self.user = User.objects.create_user(username="user", email="user@user.com", password="user")

        # Создаем курс
        self.course = Course.objects.create(title="Test course", description="Test course", owner=self.admin_user)

        # Создаем урок
        self.lesson_1 = Lesson.objects.create(title="Test lesson_1", description="Test lesson_1", course=self.course,
                                              video="https://www.youtube.com/watch?v=8sv-6AN0_cg")
        self.lesson_2 = Lesson.objects.create(title="Test lesson_2", description="Test lesson_2", course=self.course,
                                              video="https://www.youtube.com/watch?v=ozFNilK4qrc")

    def test_create_lesson(self):
        pass

    def test_create_lesson_without_permission(self):
        pass

    def test_create_lesson_with_permission(self):
        pass

    def test_update_lesson(self):
        pass

    def test_update_lesson_without_permission(self):
        pass

    def test_update_lesson_with_permission(self):
        pass

    def test_delete_lesson(self):
        pass

    def test_delete_lesson_without_permission(self):
        pass

    def test_delete_lesson_with_permission(self):
        pass

    def test_get_lesson(self):
        pass

    def test_get_lesson_without_permission(self):
        pass

    def test_get_lesson_with_permission(self):
        pass

    def test_get_lessons(self):
        pass

    def test_get_lessons_without_permission(self):
        pass

    def test_get_lessons_with_permission(self):
        pass

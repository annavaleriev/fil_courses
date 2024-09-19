from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from materials.tests.fabrics import (
    AdminUserFactory,
    UserFactory,
    ModerGroupFactory,
    LessonFactory,
)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.lesson_list_url = reverse("materials:lesson-list")


class ListLessonTestCase(LessonTestCase):
    def test__get_lessons__super_user(self):
        admin = AdminUserFactory()
        self.client.force_authenticate(user=admin)

        lessons = LessonFactory.create_batch(10)
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(lessons), response.data["count"])

        lesson_ids = {lesson.pk for lesson in lessons}
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}

        self.assertSetEqual(lesson_ids, expected_lesson_ids)

    def test__get_lessons__owner_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        count_user_owner_lessons = 3

        LessonFactory.create_batch(2)
        user_owner_lessons = LessonFactory.create_batch(
            count_user_owner_lessons, owner=user
        )
        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], count_user_owner_lessons)

        lesson_ids = {lesson.pk for lesson in user_owner_lessons}
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}

        self.assertSetEqual(lesson_ids, expected_lesson_ids)

    def test__get_lessons__moder_user(self):
        moder_group = ModerGroupFactory()
        moder = UserFactory()
        moder.groups.add(moder_group)

        user = UserFactory()

        self.client.force_authenticate(user=moder)

        count_user_owner_lessons = 3
        count_not_owner_lessons = 2

        not_owner_lessons = LessonFactory.create_batch(count_not_owner_lessons)
        user_owner_lessons = LessonFactory.create_batch(
            count_user_owner_lessons, owner=user
        )
        all_lessons = not_owner_lessons + user_owner_lessons

        response = self.client.get(self.lesson_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["count"], count_user_owner_lessons + count_not_owner_lessons
        )

        lesson_ids = {lesson.pk for lesson in all_lessons}
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}

        self.assertSetEqual(lesson_ids, expected_lesson_ids)


class CreateLessonTestCase(LessonTestCase):
    pass

    #     # Создаем пользователей тестовых
    #     self.admin_user = User.objects.create_superuser(email="admin@admin.com", password="admin")
    #     self.moder_user = User.objects.create_user(email="moder@moder.com", password="moder")
    #     self.user = User.objects.create_user(email="user@user.com", password="user")
    #
    #     # Создаем курс
    #     self.course = Course.objects.create(title="Test course", description="Test course", owner=self.admin_user)
    #
    #     # Создаем урок
    #     self.lesson_1 = Lesson.objects.create(title="Test lesson_1", description="Test lesson_1", course=self.course,
    #                                           video="https://www.youtube.com/watch?v=8sv-6AN0_cg")
    #     self.lesson_2 = Lesson.objects.create(title="Test lesson_2", description="Test lesson_2", course=self.course,
    #                                           video="https://www.youtube.com/watch?v=ozFNilK4qrc")
    #
    # def test_create_lesson(self):
    #     self.client.force_authenticate(user=self.admin_user)
    #
    #     url = reverse('materials:lesson-list')
    #
    #     # Отправляем POST запрос на подписку
    #     response = self.client.post(url, data={"video": "www.ddddd.ru", "title": "123", "course": self.course.pk})
    #     self.assertEqual(response.status_code, 400)
    #
    #     response = self.client.post(
    #         url,
    #         data={
    #             "video": "https://www.youtube.com/my_home_video/",
    #             "title": "123",
    #             "course": self.course.pk
    #         }
    #     )
    #     self.assertEqual(response.status_code, 201)

    # self.client.force_authenticate(user=None) - чтобы разлогинится

    # view = AccountDetail.as_view()
    # force_authenticate(request, user=user)
    # request = factory.post('/notes/', {'title': 'new idea'}, format='json')
    # response = view(request)
    #
    # def test_create_lesson_without_permission(self):
    #     self.client.force_authenticate(user=self.user)
    #
    #     url = reverse('materials:lesson-list')
    #
    #     response = self.client.post(
    #         url,
    #         data={
    #             "video": "https://www.youtube.com/my_home_video/",
    #             "title": "1234",
    #             "course": self.course.pk
    #         }
    #     )
    #     self.assertEqual(response.status_code, 403)  # 403 - Forbidden
    #
    # def test_create_lesson_with_permission(self):
    #     self.client.force_authenticate(user=self.moder_user)
    #
    #     self.assertTrue(
    #         self.moder_user.groups.filter(name="moders").exists())  # Проверяем что модератор в группе модераторов
    #
    #     url = reverse('materials:lesson-list')
    #
    #     response = self.client.post(
    #         url,
    #         data={
    #             "video": "https://www.youtube.com/my_home_video/",
    #             "title": "12345",
    #             "course": self.course.pk
    #         }
    #     )
    #     self.assertEqual(response.status_code, 403)  # 403 - Forbidden
    #
    # def test_update_lesson(self):
    #     self.client.force_authenticate(user=self.admin_user)  # Логинимся под админом
    #
    #     url = reverse('materials:lesson-detail', args=[self.lesson_1.pk])  # Получаем url для обновления урока
    #
    #     response = self.client.patch(url, data={"title": "Test lesson_1.1"})  # Отправляем PATCH запрос на обновление
    #     self.assertEqual(response.status_code, 200)  # Проверяем что запрос прошел успешно
    #
    # def test_update_lesson_with_permission(self):
    #     self.client.force_authenticate(user=self.moder_user)
    #     self.assertTrue(
    #         self.moder_user.groups.filter(name="moders").exists())  # Проверяем что модератор в группе модераторов
    #
    #     url = reverse('materials:lesson-detail', args=[self.lesson_1.pk])
    #     pass
    #
    # def test_update_lesson_without_permission(self):
    #     self.client.force_authenticate(user=self.user)
    #
    #     url = reverse('materials:lesson-detail', args=[self.lesson_1.pk])
    #     pass
    #
    # def test_delete_lesson(self):
    #     self.client.force_authenticate(user=self.admin_user)
    #
    #     url = reverse('materials:lesson-detail', args=[self.lesson_1.pk])
    #
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 204) # 204 - No Content - Успешное удаление
    #
    # def test_delete_lesson_without_permission(self):
    #     self.client.force_authenticate(user=self.user) # Логинимся под пользователем
    #
    #     url = reverse('materials:lesson-detail', args=[self.lesson_1.pk]) # Получаем url для удаления урока
    #
    #     response = self.client.delete(url) # Отправляем DELETE запрос на удаление
    #     self.assertEqual(response.status_code, 403) # 403 - Forbidden
    # #
    # # def test_delete_lesson_with_permission(self):
    # #     pass
    # #
    # # def test_get_lesson(self):
    # #     pass
    # #
    # # def test_get_lesson_without_permission(self):
    # #     pass
    # #
    # # def test_get_lesson_with_permission(self):
    # #     pass
    # #
    # # def test_get_lessons(self):
    # #     pass
    # #
    # # def test_get_lessons_without_permission(self):
    # #     pass
    # #
    # def test_get_lessons_with_permission(self):
    #     pass

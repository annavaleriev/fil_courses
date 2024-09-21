from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from materials.tests.fabrics import (
    AdminUserFactory,
    UserFactory,
    ModerGroupFactory,
    LessonFactory, CourseFactory,
)


class LessonTestCase(APITestCase):  # Тесты для уроков
    def setUp(self):  # Создаем клиент
        self.client = APIClient()  # Создаем клиент
        self.lesson_list_url = reverse("materials:lesson-list")  # Получаем url для списка уроков

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    def create_moder(self):
        moder_group = ModerGroupFactory()
        moder = UserFactory()
        moder.groups.add(moder_group)
        return moder

    def create_lesson(self, user, course=None, title="Test lesson",
                      video="https://www.youtube.com/watch?v=8sv-6AN0_cg"):  # Создаем урок

        if course is None:
            course = CourseFactory()
        self.authenticate_user(user)  # Логинимся под пользователем
        response = self.client.post(self.lesson_list_url, data=
        {  # Отправляем POST запрос на создание урока
            "title": title,
            "video": video,
            "course": course.pk
        })
        return response


class ListLessonTestCase(LessonTestCase):  # Тесты для списка уроков
    def test__get_lessons__super_user(self):  # Получаем уроки для суперпользователя
        admin = AdminUserFactory()  # Создаем администратора
        self.authenticate_user(admin)

        lessons = LessonFactory.create_batch(10)  # Создаем 10 уроков
        response = self.client.get(self.lesson_list_url)  # Отправляем GET запрос на список уроков

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(lessons), response.data["count"])

        lesson_ids = {lesson.pk for lesson in lessons}  # Получаем id уроков
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}  # Получаем id уроков из ответа

        self.assertSetEqual(lesson_ids, expected_lesson_ids)  # Сравниваем id уроков

    def test__get_lessons__owner_user(self):  # Получаем уроки для владельца
        user = UserFactory()  # Создаем пользователя
        self.authenticate_user(user)  # Логинимся под пользователем

        count_user_owner_lessons = 3  # Количество уроков для пользователя

        LessonFactory.create_batch(2)  # Создаем 2 урока
        user_owner_lessons = LessonFactory.create_batch(  # Создаем уроки для пользователя
            count_user_owner_lessons, owner=user  # Создаем уроки для пользователя
        )
        response = self.client.get(self.lesson_list_url)  # Отправляем GET запрос на список уроков

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем что запрос прошел успешно

        self.assertEqual(response.data["count"], count_user_owner_lessons)  # Проверяем количество уроков

        lesson_ids = {lesson.pk for lesson in user_owner_lessons}  # Получаем id уроков
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}  # Получаем id уроков из ответа

        self.assertSetEqual(lesson_ids, expected_lesson_ids)  # Сравниваем id уроков

    def test__get_lessons__moder_user(self):  # Получаем уроки для модератора
        moder = self.create_moder()  # Создаем модератора

        user = UserFactory()  # Создаем пользователя

        self.client.force_authenticate(user=moder)  # Логинимся под модератором

        count_user_owner_lessons = 3  # Количество уроков для пользователя
        count_not_owner_lessons = 2  # Количество уроков не принадлежащих пользователю

        not_owner_lessons = LessonFactory.create_batch(
            count_not_owner_lessons)  # Создаем уроки не принадлежащие пользователю
        user_owner_lessons = LessonFactory.create_batch(  # Создаем уроки для пользователя
            count_user_owner_lessons, owner=user  # Создаем уроки для пользователя
        )
        all_lessons = not_owner_lessons + user_owner_lessons  # Все уроки

        response = self.client.get(self.lesson_list_url)  # Отправляем GET запрос на список уроков

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверяем что запрос прошел успешно

        self.assertEqual(  # Проверяем количество уроков
            response.data["count"], count_user_owner_lessons + count_not_owner_lessons  # Проверяем количество уроков
        )

        lesson_ids = {lesson.pk for lesson in all_lessons}  # Получаем id уроков
        expected_lesson_ids = {lesson["id"] for lesson in response.data["results"]}  # Получаем id уроков из ответа

        self.assertSetEqual(lesson_ids, expected_lesson_ids)  # Сравниваем id уроков


class CreateLessonTestCase(LessonTestCase):  # Тесты для создания уроков

    def test__post_lessons__super_user(self):
        admin = AdminUserFactory()  # Создаем администратора
        response = self.create_lesson(admin)
        # print(response.status_code)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем что запрос прошел успешно

    def test__post_lessons__user(self):
        user = UserFactory()
        response = self.create_lesson(user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверяем что запрос прошел успешно

    def test__post_lessons__moder_user(self):
        moder = self.create_moder()  # Создаем модератора
        response = self.create_lesson(moder)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Проверяем что запрос прошел успешно


class UpdateLessonTestCase(LessonTestCase):
    def update_lesson(self, user, lesson):
        self.client.force_authenticate(user=user)
        response = self.client.patch(reverse("materials:lesson-detail", args=[lesson.pk]), data={"title": "New title"})
        return response

    def test__patch_lesson__super_user(self):
        admin = AdminUserFactory()
        lesson = LessonFactory()
        response = self.update_lesson(admin, lesson)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__patch_lesson__owner_user(self):
        user = UserFactory()
        lesson = LessonFactory(owner=user)
        response = self.update_lesson(user, lesson)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__patch_lesson__not_owner_user(self):
        user = UserFactory()
        another_user = UserFactory()
        lesson = LessonFactory(owner=another_user)
        response = self.update_lesson(user, lesson)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test__patch_lesson__moder_user(self):
        moder = self.create_moder()
        lesson = LessonFactory()
        response = self.update_lesson(moder, lesson)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteLessonTestCase(LessonTestCase):

    def test__delete_lesson__super_user(self):
        admin = AdminUserFactory() # Создаем администратора
        lesson = LessonFactory() # Создаем урок
        self.authenticate_user(admin) # Логинимся под администратором
        response = self.client.delete(reverse("materials:lesson-detail", args=[lesson.pk])) # Отправляем DELETE запрос на удаление урока
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) # Проверяем что запрос прошел успешно

    def test__delete_lesson__owner_user(self):
        user = UserFactory()
        lesson = LessonFactory(owner=user)
        self.authenticate_user(user)
        response = self.client.delete(reverse("materials:lesson-detail", args=[lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test__delete_lesson__not_owner_user(self):
        user = UserFactory()
        another_user = UserFactory()
        lesson = LessonFactory(owner=another_user)
        self.authenticate_user(user)
        response = self.client.delete(reverse("materials:lesson-detail", args=[lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test__delete_lesson__moder_user(self):
        moder = self.create_moder()
        lesson = LessonFactory()
        self.authenticate_user(moder)
        response = self.client.delete(reverse("materials:lesson-detail", args=[lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

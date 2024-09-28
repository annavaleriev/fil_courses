from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from materials.tests.fabrics import CourseFactory, UserFactory


class CourseSubscriptionTest(APITestCase):
    """Тесты для подписки на курс"""

    def setUp(self):
        self.client = APIClient()
        self.course = CourseFactory()
        self.user = UserFactory()
        self.url = reverse("materials:course-subscription", args=[self.course.pk])

    def test__add_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "подписка добавлена"})

    def test__delete__subscription(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"message": "подписка удалена"})

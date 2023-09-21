from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from users.models import Users
from users.serializers.users import UserSerializer


class UserSerializerTestCase(TestCase):
    def test_user_serializer(self):
        """
        Тестирование сериализатора UserSerializer.

        Создаем пользователя для тестирования, затем создаем сериализатор и
        проверяем, что сериализатор правильно сериализует данные пользователя.
        """
        # Создаем пользователя для тестирования
        user = Users.objects.create(email="test@example.com")

        # Создаем сериализатор и проверяем, что он правильно сериализует данные пользователя
        serializer = UserSerializer(instance=user)
        expected_data = {"email": "test@example.com"}
        self.assertEqual(serializer.data, expected_data)


class UsersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create(email="test@example.com", is_seller=False)
        self.user2 = Users.objects.create(email="test2@example.com", is_seller=True)

        # Создаем токен для пользователя и используем его для аутентификации
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_users_list_view(self):
        """
        Тестирование представления списка пользователей (UsersListView).

        Отправляем GET-запрос на список пользователей и проверяем, что получаем
        статус ответа HTTP 200 OK и ожидаемое количество пользователей.
        """
        url = reverse("users:show")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_users_detail_view(self):
        """
        Тестирование представления деталей пользователя (UsersDetailView).

        Отправляем GET-запрос на детали пользователя и проверяем, что получаем
        статус ответа HTTP 200 OK и правильный email пользователя.
        """
        url = reverse("users:detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_users_update_view(self):
        """
        Тестирование представления обновления информации пользователя (UsersUpdateView).

        Отправляем PUT-запрос на обновление информации пользователя и проверяем,
        что получаем статус ответа HTTP 200 OK и email пользователя был обновлен.
        """
        url = reverse("users:update", args=[self.user.id])
        data = {"email": "updated@example.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updated@example.com")

    def test_users_delete_view(self):
        """
        Тестирование представления удаления пользователя (UsersDeleteView).

        Отправляем DELETE-запрос на удаление пользователя и проверяем, что
        получаем статус ответа HTTP 204 No Content и пользователь был удален.
        """
        url = reverse("users:delete", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Users.objects.filter(id=self.user.id).exists())

    def test_users_registration_view(self):
        """
        Тестирование представления регистрации нового пользователя (UsersRegistrationView).

        Отправляем POST-запрос на регистрацию нового пользователя и проверяем, что
        получаем статус ответа HTTP 200 OK и пользователь был успешно создан.
        """
        url = reverse("users:registration")
        data = {
            "email": "newuser@example.com",
            "password": "password123",
            "password2": "password123",
            "is_seller": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["response"], True)
        self.assertTrue(Users.objects.filter(email="newuser@example.com").exists())

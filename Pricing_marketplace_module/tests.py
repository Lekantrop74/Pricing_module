from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from users.models import Users


class CalculatePriceViewTestCase(TestCase):
    def setUp(self):
        """
        Подготовка к тестированию. Создаем пользователя, аутентифицируем его и создаем клиента API.
        """
        self.user = Users(
            email="test@gmail.com",
            password="test",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            is_seller=True,
        )

        self.user.set_password("test")
        self.user.save()

        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_calculate_price(self):
        """
        Тестирование расчета цены при создании товара.

        Создаем товар с заданной ценой и проверяем, что расчет цены происходит правильно.
        """
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": "10.00"
        }

        response = self.client.post('/calculate_price/', data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Итоговая цена", response.data)

        # Проверяем, что цена правильно рассчитана с помощью assertAlmostEqual
        calculated_price = float(response.data["Итоговая цена"])
        expected_price = 10.0 + (0.06 * 10.0) + (0.02 * 10.0) + (0.10 * 10.0) + (0.20 * 10.0)
        self.assertAlmostEqual(calculated_price, expected_price, delta=0.01)

    def test_unauthenticated_create_product(self):
        """
        Тест на создание товара без аутентификации.

        Попытка создания товара без предоставления аутентификации должна вернуть 401 Unauthorized.
        """
        client = APIClient()
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": "10.00"
        }
        response = client.post('/calculate_price/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_required_fields(self):
        """
        Тест на отсутствие обязательных полей.

        Попытка создания товара без указания обязательного поля "name" должна вернуть 400 Bad Request.
        """
        data = {
            "description": "Test Description",
            "price": "10.00"
        }
        response = self.client.post('/calculate_price/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # Проверяем наличие ошибки для поля "name"

    def test_negative_price(self):
        """
        Тест на отрицательную цену.

        Попытка создания товара с отрицательной ценой должна вернуть 400 Bad Request.
        """
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": "-10.00"
        }
        response = self.client.post('/calculate_price/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Цена товара не может быть отрицательной", response.data["detail"])

    def test_calculate_price_with_zero_price(self):
        """
        Тест на расчет цены с нулевой ценой.

        Создаем товар с нулевой ценой и проверяем, что итоговая цена равна 0.0.
        """
        data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": "0.00"
        }
        response = self.client.post('/calculate_price/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEqual(float(response.data["Итоговая цена"]), 0.0, places=2)

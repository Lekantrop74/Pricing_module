from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from Pricing_marketplace_module.serializers import ProductSerializer

# Константы для ставок комиссий
TAX_RATE = 0.06
BANK_COMMISSION_RATE = 0.02
AUTHOR_COMMISSION_RATE = 0.10
MARKETPLACE_COMMISSION_RATE = 0.20


class CalculatePriceView(generics.CreateAPIView):
    """
    API View для создания объекта товара с автоматическим расчетом цены и сохранением.

    Serializer: ProductSerializer
    Permission: Только аутентифицированным пользователям разрешено использовать этот эндпоинт.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def calculate_total_price(self, price):
        """
        Выполняет расчет итоговой цены на основе заданной цены товара.

        Args:
            price (float): Цена товара.

        Returns:
            float: Итоговая цена.

        """
        total_price = price + (TAX_RATE * price) + (BANK_COMMISSION_RATE * price) + \
                      (AUTHOR_COMMISSION_RATE * price) + (MARKETPLACE_COMMISSION_RATE * price)
        return round(total_price, 2)

    def create(self, request, *args, **kwargs):
        """
        Обработка HTTP POST-запроса для создания объекта товара с автоматическим расчетом цены.

        Args:
            request (HttpRequest): Запрос от клиента.

        Returns:
            Response: HTTP-ответ с итоговой ценой объекта товара.

        """
        # Извлекаем цену из запроса
        price = request.data.get('price', None)
        if price is None:
            return Response({'detail': 'Цена товара не указана'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = float(price)  # Преобразуем значение в число с плавающей запятой
            if price < 0:
                return Response({'detail': 'Цена товара не может быть отрицательной'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Цена товара должна быть числом'}, status=status.HTTP_400_BAD_REQUEST)

        # Рассчитываем итоговую цену
        total_price = self.calculate_total_price(price)

        return Response({'Итоговая цена': total_price}, status=status.HTTP_201_CREATED)

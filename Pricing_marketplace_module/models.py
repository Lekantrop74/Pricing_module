from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Метод для представления модели в виде строки
    def __str__(self):
        return f"Продукт: {self.name} "

    # Метаданные модели
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = 'Продукты'

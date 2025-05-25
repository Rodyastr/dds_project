from django.db import models
from django.utils import timezone

class Status(models.Model):
    """
    Модель для статусов записей
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name

class FlowType(models.Model):
    """
    Модель для типов потоков
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Модель для категорий, которая связана с типами потоков
    """
    name = models.CharField(max_length=100, verbose_name="Категория")
    flow_type = models.ForeignKey(FlowType, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип потока", null=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('name', 'flow_type')  # Позволяет иметь одинаковые категории с разными потоками

    def __str__(self):
        return f"{self.name} ({self.flow_type.name})"

class SubCategory(models.Model):
    """
    Модель подкатегорий
    """
    name = models.CharField(max_length=100, verbose_name="Подкатегория")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ('name', 'category') # Позволяет иметь одинаковые подкатегории с разными категориями

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class CashFlow(models.Model):
    """
    Модель по движению дежненых средств
    """
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    flow_type = models.ForeignKey(FlowType, on_delete=models.CASCADE, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма (₽)")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ['-date'] # Сортировка по дате по убыванию

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%Y')} - {self.flow_type.name}: {self.amount} ₽"
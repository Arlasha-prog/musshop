from decimal import Decimal
from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Пользователь",
    )
    # данные покупателя
    customer_name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=50)
    address = models.CharField("Адрес", max_length=255, blank=True)
    comment = models.TextField("Комментарий", blank=True)

    # служебные поля
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Обновлён", auto_now=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=[
            ("new", "Новый"),
            ("processing", "В обработке"),
            ("done", "Завершён"),
            ("cancelled", "Отменён"),
        ],
        default="new",
    )

    # можно хранить зафиксированную сумму заказа (заполняем после оформления)
    total_amount = models.DecimalField(
        "Итоговая сумма",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.pk}"

    # --- Суммы ---
    def total(self) -> Decimal:
        """Расчёт суммы «на лету» по позициям (без учёта total_amount)."""
        return sum((item.total() for item in self.items.all()), start=Decimal("0"))

    @property
    def total_value(self) -> Decimal:
        """
        Универсально получить сумму:
        - если total_amount уже сохранен — отдаём его,
        - иначе считаем по позициям.
        """
        if self.total_amount is not None:
            return self.total_amount
        return self.total()

    def items_count(self) -> int:
        """Количество всех товаров в заказе"""
        return sum((item.qty or 0) for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Товар"
    )
    price = models.DecimalField("Цена на момент заказа", max_digits=12, decimal_places=2)
    qty = models.PositiveIntegerField("Кол-во", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product} x {self.qty}"

    def total(self) -> Decimal:
        """Сумма по позиции, с безопасными значениями."""
        price = self.price or Decimal("0")
        qty = self.qty or 0
        return price * Decimal(qty)

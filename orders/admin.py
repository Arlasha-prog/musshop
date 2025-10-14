from django.contrib import admin
from .models import Order, OrderItem


# ----- Inline для позиций заказа -----
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ("product", "price", "qty", "line_total")
    readonly_fields = ("product", "price", "qty", "line_total")

    def line_total(self, obj):
        # безопасно считаем строку, если что-то None
        price = obj.price or 0
        qty = obj.qty or 0
        return price * qty

    line_total.short_description = "Сумма строки"


# ----- Админка заказа -----
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    # верхняя таблица
    list_display = ("id", "created", "customer_name", "phone", "total_amount_display")
    list_display_links = ("id", "customer_name")
    search_fields = ("id", "customer_name", "phone", "address")
    list_filter = ("created", "updated")
    date_hierarchy = "created"
    ordering = ("-created",)

    # форма редактирования заказа
    readonly_fields = ("created", "updated", "calculated_total")
    fieldsets = (
        ("Данные клиента", {
            "fields": ("customer_name", "phone", "address", "comment"),
        }),
        ("Служебное", {
            "fields": ("created", "updated", "calculated_total"),
        }),
    )

    # вычисляемая сумма заказа (по позициям)
    def _calc_total(self, order: Order):
        return sum(
            (item.price or 0) * (item.qty or 0)
            for item in order.items.all()
        )

    def total_amount_display(self, order: Order):
        return self._calc_total(order)

    total_amount_display.short_description = "Сумма заказа"

    def calculated_total(self, order: Order):
        """Поле только для чтения внутри формы заказа."""
        return self._calc_total(order)

    calculated_total.short_description = "Итого (рассчитано)"

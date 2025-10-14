# catalog/filters.py
from django.contrib.admin import SimpleListFilter

class PriceRangeFilter(SimpleListFilter):
    title = "Цена (диапазон)"
    parameter_name = "price_range"

    # Кастомный шаблон фильтра (создадим ниже)
    template = "admin/inputs/price_range_filter.html"

    def lookups(self, request, model_admin):
        return ()  # не показываем стандартные пункты

    def queryset(self, request, queryset):
        min_price = request.GET.get("price_min")
        max_price = request.GET.get("price_max")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

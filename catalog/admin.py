# catalog/admin.py
from django.contrib import admin, messages
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import Category, Product, APIKey
from .forms import ProductAdminForm
from .filters import PriceRangeFilter

# ===== Actions =====
@admin.action(description="Сделать активными")
def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    messages.success(request, f"Обновлено: {updated}")

@admin.action(description="Сделать неактивными")
def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    messages.success(request, f"Обновлено: {updated}")

@admin.action(description="Экспортировать в CSV")
def export_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [f.name for f in meta.fields]
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{meta.model_name}.csv"'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = []
        for field in field_names:
            val = getattr(obj, field)
            row.append(str(val))
        writer.writerow(row)
    return response

# ===== Category =====
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "products_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    list_per_page = 25

    @admin.display(description="Товаров")
    def products_count(self, obj):
        # Не завися от related_name:
        return Product.objects.filter(category=obj).count()

# ===== Product =====
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = (
        "thumb", "title", "category", "price_formatted",
        "is_active", "created_at",
    )
    list_display_links = ("thumb", "title")
    list_editable = ("is_active",)
    list_filter = (
        "is_active", "category",
        PriceRangeFilter,
        ("created_at", admin.DateFieldListFilter),
    )
    search_fields = ("title", "slug", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "image_tag")
    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "category", "price", "is_active")
        }),
        ("Контент", {
            "fields": ("short_desc", "description"),
            "description": "Описание выводится на странице товара. Краткая версия может использоваться в карточках или предпросмотре."
        }),
        ("Медиа", {
            "fields": ("image", "image_tag"),
            "description": "Загрузите изображение товара. Превью ниже появится после сохранения."
        }),
        ("Служебное", {
            "fields": ("created_at",),
        }),
    )
    save_on_top = True
    ordering = ("-created_at",)
    list_per_page = 30
    actions = [make_active, make_inactive, export_csv]

    @admin.display(description="Превью")
    def thumb(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html(
                    '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;">',
                    obj.image.url,
                )
            except Exception:
                return "—"
        return "—"

    @admin.display(description="Цена")
    def price_formatted(self, obj):
        if obj.price is None:
            return "—"
        return f"{int(obj.price):,} ₸".replace(",", " ")

    @admin.display(description="Превью (большое)")
    def image_tag(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html(
                    '<img src="{}" style="max-width:240px;border-radius:10px;">',
                    obj.image.url,
        )
            except Exception:
                return "—"
        return "—"


@admin.action(description="Пересоздать выбранные ключи")
def regenerate_keys(modeladmin, request, queryset):
    regenerated = 0
    for api_key in queryset:
        api_key.regenerate()
        regenerated += 1
    if regenerated:
        modeladmin.message_user(
            request,
            f"Обновлено ключей: {regenerated}",
            messages.SUCCESS,
        )
    else:
        modeladmin.message_user(
            request,
            "Нет ключей для обновления",
            messages.WARNING,
        )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "preview_key", "is_active", "created_at", "updated_at")
    readonly_fields = ("key", "created_at", "updated_at")
    search_fields = ("name", "key")
    list_filter = ("is_active", "created_at")
    actions = [regenerate_keys]
    ordering = ("-created_at",)

    @admin.display(description="Ключ")
    def preview_key(self, obj: APIKey):
        if not obj.key:
            return "—"
        if len(obj.key) <= 10:
            return obj.key
        return f"{obj.key[:6]}…{obj.key[-4:]}"

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Только реальные поля модели:
        fields = ["customer_name", "phone", "address", "comment"]

        labels = {
            "customer_name": "Имя",
            "phone": "Телефон",
            "address": "Адрес",
            "comment": "Комментарий к заказу",
        }

        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Как к вам обращаться",
                "required": "required",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+7 777 000 00 00",
                "required": "required",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Город, улица, дом, кв.",
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Пожелания к доставке",
            }),
        }

    def clean_phone(self):
        """Лёгкая нормализация телефона (по желанию — можно убрать)."""
        phone = (self.cleaned_data.get("phone") or "").strip()
        # простая очистка пробелов
        phone = " ".join(phone.split())
        return phone

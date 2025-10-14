from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def _style_user_creation_form(form: UserCreationForm) -> UserCreationForm:
    # Добавляем классы Bootstrap и плейсхолдеры
    form.fields["username"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "например, musshop_user",
    })
    form.fields["password1"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "••••••••",
    })
    form.fields["password2"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "повторите пароль",
    })
    return form


def register(request):
    if request.method == "POST":
        form = _style_user_creation_form(UserCreationForm(request.POST))
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = _style_user_creation_form(UserCreationForm())
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by("-created")
    return render(request, "accounts/profile.html", {"orders": orders})


@login_required
def edit_profile(request):
    class SimpleUserChangeForm(UserChangeForm):
        class Meta(UserChangeForm.Meta):
            fields = ("first_name", "last_name", "email")

    if request.method == "POST":
        form = SimpleUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = SimpleUserChangeForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})


def logout_view(request):
    """Logout that accepts both POST and GET for convenience (handles 405 issue)."""
    if request.method in ("POST", "GET"):
        logout(request)
        return redirect("home")
    # Fallback just in case
    return redirect("home")

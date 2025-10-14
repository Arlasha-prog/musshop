from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404

from .models import Product, Category


def home(request):
    """Главная — сейчас без товарных блоков (как договаривались)."""
    return render(request, "index.html")


def _apply_search_and_sort(qs, request):
    """Общая логика фильтрации и сортировки."""
    # поиск
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # сортировка
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-created_at")
    else:
        qs = qs.order_by("-created_at")

    return qs, query, sort


def all_products(request):
    """Страница каталога со всеми товарами."""
    categories = Category.objects.all().order_by("name")
    qs = Product.objects.filter(is_active=True)
    qs, query, sort = _apply_search_and_sort(qs, request)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "properties.html",
        {
            "products": page_obj,
            "categories": categories,
            "category": None,
            "query": query,
            "sort": sort,
        },
    )


def category_list(request, slug):
    """Каталог в конкретной категории."""
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all().order_by("name")
    qs = Product.objects.filter(is_active=True, category=category)
    qs, query, sort = _apply_search_and_sort(qs, request)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "properties.html",
        {
            "products": page_obj,
            "categories": categories,
            "category": category,
            "query": query,
            "sort": sort,
        },
    )


def product_detail(request, slug):
    """Карточка товара + похожие товары."""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Похожие товары: из той же категории, кроме текущего
    related = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(id=product.id)[:3]
    )

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related": related,
        },
    )


def flatpage(request, page):
    """
    Отдаём любой статический шаблон вида <slug>.html
    Например: contact.html, about.html и т.д.
    """
    return render(request, f"{page}.html")


# ====== API (JSON) ======
def api_categories(request):
    categories = (
        Category.objects.annotate(
            active_products=Count("products", filter=Q(products__is_active=True))
        )
        .order_by("name")
    )
    data = []
    for category in categories:
        featured = (
            category.products.filter(is_active=True).order_by("-created_at").first()
        )
        data.append(
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "products_active": category.active_products,
                "featured_product": {
                    "id": featured.id,
                    "title": featured.title,
                    "slug": featured.slug,
                    "price": float(featured.price)
                    if getattr(featured, "price", None) is not None
                    else None,
                    "image": featured.image.url if getattr(featured, "image", None) else None,
                }
                if featured
                else None,
            }
        )
    return JsonResponse(data, safe=False)


def api_products(request):
    qs = Product.objects.filter(is_active=True).order_by("-created_at")
    data = [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "price": float(p.price) if p.price is not None else None,
            "image": p.image.url if getattr(p, "image", None) else None,
            "category": {
                "id": p.category.id,
                "name": p.category.name,
                "slug": p.category.slug,
            } if p.category_id else None,
        }
        for p in qs
    ]
    return JsonResponse(data, safe=False)


def api_product_detail(request, pk: int):
    try:
        p = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    data = {
        "id": p.id,
        "title": p.title,
        "slug": p.slug,
        "price": float(p.price) if p.price is not None else None,
        "image": p.image.url if getattr(p, "image", None) else None,
        "description": p.description,
        "category": {
            "id": p.category.id,
            "name": p.category.name,
            "slug": p.category.slug,
        } if p.category_id else None,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }
    return JsonResponse(data)

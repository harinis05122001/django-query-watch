# examples/demo_project/shop/views.py

import json
from django.http import JsonResponse
from .models import Product


def bad_products(request):
    """
    Intentionally bad view.
    Triggers N+1 queries — one extra query per product to fetch category.
    """
    products = Product.objects.all()
    data = []
    for product in products:
        data.append(
            {
                "name": product.name,
                "price": str(product.price),
                "category": product.category.name,  # N+1 happens here
            }
        )
    return JsonResponse({"products": data})


def good_products(request):
    """
    Optimized view.
    Uses select_related to fetch everything in one query.
    """
    products = Product.objects.select_related("category").all()
    data = []
    for product in products:
        data.append(
            {
                "name": product.name,
                "price": str(product.price),
                "category": product.category.name,
            }
        )
    return JsonResponse({"products": data})


def health(request):
    return JsonResponse({"status": "ok"})

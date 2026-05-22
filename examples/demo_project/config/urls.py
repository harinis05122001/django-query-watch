# examples/demo_project/config/urls.py

from django.urls import path
from shop import views

urlpatterns = [
    path("api/products/bad/", views.bad_products, name="bad-products"),
    path("api/products/good/", views.good_products, name="good-products"),
    path("api/health/", views.health, name="health"),
]

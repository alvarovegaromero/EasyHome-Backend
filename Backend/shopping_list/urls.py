from django.urls import path

from .views.product_bought_in_range_view import ProductBoughtInRangeAPIView
from .views.product_list_create_view import ProductListCreateAPIView
from .views.product_mark_to_buy_view import ProductMarkToBuyAPIView
from .views.product_to_buy_list_view import ProductToBuyListAPIView
from .views.product_to_buy_mark_as_bought_view import ProductToBuyMarkAsBoughtAPIView
from .views.product_update_delete_view import ProductUpdateDeleteAPIView

urlpatterns = [
    path("<int:group_id>/products", ProductListCreateAPIView.as_view(), name="products"),
    path(
        "<int:group_id>/products/<int:product_id>",
        ProductUpdateDeleteAPIView.as_view(),
        name="product",
    ),
    path(
        "<int:group_id>/products/<int:product_id>/to_buy",
        ProductMarkToBuyAPIView.as_view(),
        name="mark_product_to_buy",
    ),
    path(
        "<int:group_id>/products/to_buy", ProductToBuyListAPIView.as_view(), name="products_to_buy"
    ),
    path(
        "<int:group_id>/products/bought",
        ProductToBuyMarkAsBoughtAPIView.as_view(),
        name="mark_product_as_bought",
    ),
    path(
        "<int:group_id>/products/bought/range",
        ProductBoughtInRangeAPIView.as_view(),
        name="retrieve_bought_products_in_range",
    ),
]

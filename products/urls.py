from django.urls import path

from products.views import CategoryListView, ProductListView, ProductDetailView, ReviewListCreateView, \
    toggle_like_review, ToggleLikeProductView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<uuid:id>', ProductDetailView.as_view(), name='product-detail'),
    path('reviews/<uuid:id>', ReviewListCreateView.as_view(), name='review-list-create'),
    path('products/<uuid:product_id>/like/', ToggleLikeProductView.as_view(), name='toggle-like-product'),
    path('reviews/<uuid:review_id>/like/', toggle_like_review, name='toggle-like-review'),
]

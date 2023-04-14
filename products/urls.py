from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path('', views.home_product, name="home"),
    path('upload/product/',views.upload_product_view, name="upload"),
    path('manage/product/<slug>/', views.product_manage_detil, name="manage"),
    path('delete-image/<pk>/', views.delete_image_view, name="delete_image"),
    path('upload-image/<pk>/', views.upload_image, name="upload_image"),
    path('not-found/', views.not_found_page, name="not_found"),
    path('detail-product/<slug>/', views.detail_product_view, name="detail_product")
]
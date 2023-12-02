from django.urls import path
from . import views

urlpatterns = [
    path('execute_scrapper/', views.scrapper2),
    path('request_scrapper/', views.request_scrapper),
    path('scrapper_requests/', views.get_all_scrap_requests,),
    path('scrapper_requests/<str:pk>/', views.get_ind_scrap_request,),
    path('products/', views.get_all_products),
    path('products/<str:pk>/', views.get_ind_product),
    path('update_product/<str:pk>/', views.update_ind_product),
    path('create_ind_product/', views.create_ind_product),
    # path('worker/', views.worker),
]
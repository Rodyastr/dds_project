from django.urls import path
from . import views

urlpatterns = [
    # Главная страница со списком записей ДДС
    path('', views.cash_flow_list, name='cash_flow_list'),

    # Маршруты по созданию, редактированию и удалению записей
    path('create/', views.cash_flow_create, name='cash_flow_create'),
    path('edit/<int:pk>/', views.cash_flow_edit, name='cash_flow_edit'),
    path('delete/<int:pk>/', views.cash_flow_delete, name='cash_flow_delete'),

    # Маршруты для справочников
    path('dictionaries/', views.dictionary_management, name='dictionary_management'),
    path('dictionaries/status/create/', views.status_create, name='status_create'),
    path('dictionaries/status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('dictionaries/status/delete/<int:pk>/', views.status_delete, name='status_delete'),

    path('dictionaries/flow_type/create/', views.flow_type_create, name='flow_type_create'),
    path('dictionaries/flow_type/edit/<int:pk>/', views.flow_type_edit, name='flow_type_edit'),
    path('dictionaries/flow_type/delete/<int:pk>/', views.flow_type_delete, name='flow_type_delete'),

    path('dictionaries/category/create/', views.category_create, name='category_create'),
    path('dictionaries/category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('dictionaries/category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('dictionaries/subcategory/create/', views.subcategory_create, name='subcategory_create'),
    path('dictionaries/subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('dictionaries/subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),

    # AJAX маршруты
    path('ajax/load_categories/', views.load_categories, name='ajax_load_categories'),
    path('ajax/load_subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
]
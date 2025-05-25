from django.contrib import admin
from .models import Status, FlowType, Category, SubCategory, CashFlow

# Регистрация моделей в административной панели Django для удобного управления.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FlowType)
class FlowTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flow_type')
    list_filter = ('flow_type',)
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'flow_type', 'category', 'subcategory', 'amount')
    list_filter = ('status', 'flow_type', 'category', 'subcategory', 'date')
    search_fields = ('comment',)
    date_hierarchy = 'date'
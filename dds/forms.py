from django import forms
from .models import CashFlow, Status, FlowType, Category, SubCategory

class CashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей движения денежных средств
    """
    date = forms.DateTimeField(
        label="Дата создания",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )


    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'flow_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': '1000.00'})
        }

    # Инициализация формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Динамическая фильтрация категорий и подкатегорий
        if 'flow_type' in self.data:
            try:
                flow_type_id = int(self.data.get('flow_type'))
                self.fields['category'].queryset = Category.objects.filter(flow_type_id=flow_type_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['category'].queryset = Category.objects.none()
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.flow_type.categories.order_by('name')
        else:
            self.fields['category'].queryset = Category.objects.none()
        # 2. Динамическая фильтрация подкатегорий по выбранной категории.
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()

        # Помечаем основные поля, как обязательные
        for field_name in ['status', 'flow_type', 'category', 'subcategory', 'amount']:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        flow_type = cleaned_data.get('flow_type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if flow_type and category and category.flow_type != flow_type:
            self.add_error('category', 'Выбранная категория не соответствует выбранному типу.')

        if category and subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Выбранная подкатегория не относится к выбранной категории.')

        return cleaned_data

# Формы для управления справочником, создаются автоматически на основе моделей
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class FlowTypeForm(forms.ModelForm):
    class Meta:
        model = FlowType
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'flow_type']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
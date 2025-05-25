from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import CashFlow, Status, FlowType, Category, SubCategory
from .forms import CashFlowForm, StatusForm, FlowTypeForm, CategoryForm, SubCategoryForm
from datetime import datetime

def cash_flow_list(request):
    """
    Главная страница со списком всех записей ДДС и фильтрами
    """
    cash_flows = CashFlow.objects.all()

    # Получаем параметры фильтрации из GET-запроса
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    status_id = request.GET.get('status')
    flow_type_id = request.GET.get('flow_type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    # Фильтрация по диапазону дат
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            cash_flows = cash_flows.filter(date__gte=start_date)
        except ValueError:
            pass # Игнорируем неверный формат даты
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            cash_flows = cash_flows.filter(date__lte=end_date)
        except ValueError:
            pass # Игнорируем неверный формат даты

    # Применение фильтров из GET-запроса
    if status_id:
        cash_flows = cash_flows.filter(status_id=status_id)
    if flow_type_id:
        cash_flows = cash_flows.filter(flow_type_id=flow_type_id)
    if category_id:
        cash_flows = cash_flows.filter(category_id=category_id)
    if subcategory_id:
        cash_flows = cash_flows.filter(subcategory_id=subcategory_id)

    statuses = Status.objects.all()
    flow_types = FlowType.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    # Для динамической фильтрации категорий и подкатегорий
    selected_flow_type = None
    if flow_type_id:
        try:
            selected_flow_type = FlowType.objects.get(pk=flow_type_id)
            categories = categories.filter(flow_type=selected_flow_type)
        except FlowType.DoesNotExist:
            pass

    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(pk=category_id)
            subcategories = subcategories.filter(category=selected_category)
        except Category.DoesNotExist:
            pass


    context = {
        'cash_flows': cash_flows,
        'statuses': statuses,
        'flow_types': flow_types,
        'categories': categories,
        'subcategories': subcategories,
        'selected_status': status_id,
        'selected_flow_type': flow_type_id,
        'selected_category': category_id,
        'selected_subcategory': subcategory_id,
        'start_date': start_date_str,
        'end_date': end_date_str,
    }
    return render(request, 'dds/cash_flow_list.html', context)

# Представление для создания новой записи ДДС
def cash_flow_create(request):
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cash_flow_list') # После сохранения перенаправляем на основной список операций
    else:
        form = CashFlowForm()
    return render(request, 'dds/cash_flow_form.html', {'form': form, 'title': 'Создать запись ДДС'})

# Представление для редактирования существующей записи ДДС
def cash_flow_edit(request, pk):
    cash_flow = get_object_or_404(CashFlow, pk=pk) # Получаем запись по ID, либо вызывается исключение 404
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cash_flow)
        if form.is_valid():
            form.save()
            return redirect('cash_flow_list')
    else:
        # Передаем дату в нужном формате для datetime-local
        initial_date = cash_flow.date.strftime('%Y-%m-%dT%H:%M')
        form = CashFlowForm(instance=cash_flow, initial={'date': initial_date})
    return render(request, 'dds/cash_flow_form.html', {'form': form, 'title': 'Редактировать запись ДДС'})

# Представление для удаления записи ДДС
def cash_flow_delete(request, pk):
    cash_flow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cash_flow.delete()
        return redirect('cash_flow_list')
    return render(request, 'dds/cash_flow_confirm_delete.html', {'cash_flow': cash_flow})

# Управление справочниками
def dictionary_management(request):
    statuses = Status.objects.all()
    flow_types = FlowType.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, 'dds/dictionary_management.html', {
        'statuses': statuses,
        'flow_types': flow_types,
        'categories': categories,
        'subcategories': subcategories
    })

# Операции по созданию, редактированию, удалению типов
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = StatusForm()
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Добавить статус'})

def status_edit(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = StatusForm(instance=status)
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Редактировать статус'})

def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('dictionary_management')
    return render(request, 'dds/dictionary_confirm_delete.html', {'item': status, 'item_type': 'статус'})

# Операции по созданию, редактированию, удалению типов
def flow_type_create(request):
    if request.method == 'POST':
        form = FlowTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = FlowTypeForm()
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Добавить тип'})

def flow_type_edit(request, pk):
    flow_type = get_object_or_404(FlowType, pk=pk)
    if request.method == 'POST':
        form = FlowTypeForm(request.POST, instance=flow_type)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = FlowTypeForm(instance=flow_type)
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Редактировать тип'})

def flow_type_delete(request, pk):
    flow_type = get_object_or_404(FlowType, pk=pk)
    if request.method == 'POST':
        # Проверяем, есть ли зависимые категории
        if flow_type.categories.exists():
            return render(request, 'dds/dictionary_confirm_delete.html', {
                'item': flow_type,
                'item_type': 'тип',
                'error_message': 'Нельзя удалить тип, так как с ним связаны категории. Сначала удалите или перенесите их.'
            })
        flow_type.delete()
        return redirect('dictionary_management')
    return render(request, 'dds/dictionary_confirm_delete.html', {'item': flow_type, 'item_type': 'тип'})

# Операции по созданию, редактированию, удалению категорий
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = CategoryForm()
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Добавить категорию'})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Редактировать категорию'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        # Проверяем, есть ли зависимые подкатегории или записи ДДС
        if category.subcategories.exists():
            return render(request, 'dds/dictionary_confirm_delete.html', {
                'item': category,
                'item_type': 'категорию',
                'error_message': 'Нельзя удалить категорию, так как с ней связаны подкатегории. Сначала удалите или перенесите их.'
            })
        if category.cashflow_set.exists(): # Проверяем связанные записи CashFlow
            return render(request, 'dds/dictionary_confirm_delete.html', {
                'item': category,
                'item_type': 'категорию',
                'error_message': 'Нельзя удалить категорию, так как с ней связаны записи ДДС. Сначала удалите или перенесите их.'
            })
        category.delete()
        return redirect('dictionary_management')
    return render(request, 'dds/dictionary_confirm_delete.html', {'item': category, 'item_type': 'категорию'})

# Операции по созданию, редактированию, удалению подкатегорий
def subcategory_create(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = SubCategoryForm()
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Добавить подкатегорию'})

def subcategory_edit(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('dictionary_management')
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'dds/dictionary_form.html', {'form': form, 'title': 'Редактировать подкатегорию'})

def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        # Проверяем, есть ли зависимые записи ДДС
        if subcategory.cashflow_set.exists(): # Проверяем связанные записи CashFlow
            return render(request, 'dds/dictionary_confirm_delete.html', {
                'item': subcategory,
                'item_type': 'подкатегорию',
                'error_message': 'Нельзя удалить подкатегорию, так как с ней связаны записи ДДС. Сначала удалите или перенесите их.'
            })
        subcategory.delete()
        return redirect('dictionary_management')
    return render(request, 'dds/dictionary_confirm_delete.html', {'item': subcategory, 'item_type': 'подкатегорию'})

# AJAX-эндпоинт для динамической загрузки категорий на основе выбранного типа
def load_categories(request):
    flow_type_id = request.GET.get('flow_type_id')
    categories = Category.objects.filter(flow_type_id=flow_type_id).order_by('name')
    return JsonResponse(list(categories.values('id', 'name')), safe=False)

# AJAX-эндпоинт для динамической загрузки подкатегорий на основе выбранной категории
def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)
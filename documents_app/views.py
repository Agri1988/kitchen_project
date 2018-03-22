from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from .products_movement import product_movement, product_movement_dish

from .models import Document, ProductsInDocument, DishInDocument, MovingProducts
from dish_app.models import Product, Dish, ProductCategory
from .forms import DocumentForm, DishInDocumentForm, ProductInDocumentsForm

# Create your views here.
@login_required(login_url='users_app:login')
def all_documents(request):
    documents = Document.objects.all()
    context = {'documents':documents}
    return render(request, 'documents_app/all_documents.html', context)


@login_required(login_url='users_app:login')
def detail_document(request, document_id = None):
    if document_id != None:
        document = Document.objects.get(id=document_id)
        products = ProductsInDocument.objects.filter(document_id=document_id)
        dishes = DishInDocument.objects.filter(document_id=document_id)
        productsInDocument = [[ProductInDocumentsForm(instance=product),product.id, product.data.get_unit_display]
                              for product in products]
        dishesInDocument = [[DishInDocumentForm(instance=dish), dish.id] for dish in dishes]
        #print(products, dishes, dishesInDocument)
    else:
        document = None
        products = None
        dishes = None
        productsInDocument = None
        dishesInDocument = None

    if request.method != 'POST':
        form = DocumentForm(instance=document)
    else:
        moves = MovingProducts.objects.filter(document_id=document_id)
        print(moves, request.POST)
        if request.POST['document_type'] == '0':
            product_movement(request, moves, products, document)
        elif request.POST['document_type'] == '1':
            product_movement(request, moves, product_movement_dish(DishInDocument.objects.filter(document_id=document_id)), document)
        form = DocumentForm(instance=document, data=request.POST)
        if form.is_valid():
            if document_id == None:
                new_document = form.save()
                new_id = new_document.id
                #print(new_id)
                return HttpResponseRedirect(reverse('documents_app:detail_document', args=[new_id]))
            form.save()

    context = {'form': form, 'document_id': document_id, 'products': products, 'dishes': dishes,
               'productsInDocument': productsInDocument if productsInDocument or productsInDocument == None else False,
               'dishesInDocument': dishesInDocument}
    if document_id == None:
        context.update({'new': True})

    return render(request, 'documents_app/detail_document.html', context)



@login_required(login_url='users_app:login')
def get_all_dishes_to_document(request):
    if request.POST.get('object_id'):
        new_entry = DishInDocument()
        new_entry.data = Dish.objects.get(id=request.POST['object_id'])
        new_entry.document = Document.objects.get(id=request.POST['document_id'])
        new_entry.count = request.POST['count']
        new_entry.save()
        dishInDocument = [DishInDocumentForm(instance=new_entry), new_entry.id ]
        template = get_template('documents_app/detail_document_product_or_dish.html')
        product_movement_dish(DishInDocument.objects.filter(document_id=new_entry.document.id))
        return HttpResponse(template.render({'datas': dishInDocument, 'one_line':True}, request))
    else:
        dishes = Dish.objects.all()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'add_dish':True, 'dishes':dishes,
                                             'url':'/documents/get_all_dishes_to_document/'}, request))


@login_required(login_url='users_app:login')
def delete_protuct_from_document():
    pass


@login_required(login_url='users_app:login')
def get_all_products_to_document(request):
    if request.POST.get('object_id'):
        new_entry = ProductsInDocument()
        new_entry.data = Product.objects.get(id=request.POST['object_id'])
        new_entry.document = Document.objects.get(id=request.POST['document_id'])
        new_entry.count = request.POST['count']
        new_entry.save()
        productInDocument = [ProductInDocumentsForm(instance=new_entry), new_entry.id, new_entry.data.get_unit_display]
        template = get_template('documents_app/detail_document_product_or_dish.html')
        product_movement_dish(DishInDocument.objects.filter(document_id=new_entry.document.id))
        return HttpResponse(template.render({'datas': productInDocument, 'one_line': True}, request))
    elif request.POST.get('ajax'):
        product = Product()
        product.name = request.POST['name']
        product.unit = request.POST['unit']
        product.category = ProductCategory.objects.get(id=request.POST['category'])
        product.save()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'dish': product, 'line_number': request.POST['line_number'],
                                             'url': '/documents/get_all_products_to_document/'}, request))
    else:
        products = Product.objects.all()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'add_product':True, 'dishes':products,
                                             'url':'/documents/get_all_products_to_document/'}, request))


@login_required(login_url='users_app:login')
def products_remnants(request, document_id = None, document_date = date.today().strftime('%d.%m.%Y')):
    print(request.POST, document_id, document_date)
    date_to_filter_fireld = document_date
    document_date = document_date.split('.')
    document_date.reverse()
    document_date = '-'.join(document_date)
    storage_field = DocumentForm()
    movement_entries = MovingProducts.objects.filter(date__lte=document_date)

    products = Product.objects.all()
    remnants_of_products = {}
    for product in products:
        product_id_inloop = product.id
        for product_entry in movement_entries:
            product_count = product_entry.count
            if (product_entry.document.document_type =='1'):
                product_count = product_count * (-1)
            if (product_id_inloop == product_entry.product.id) and (product_entry.operation_status == True):
                if product_id_inloop not in remnants_of_products:
                    remnants_of_products[product_id_inloop] = Decimal(product_count).quantize(Decimal("1.000"))
                else:
                    remnants_of_products[product_id_inloop] += Decimal(product_count).quantize(Decimal("1.000"))
    temp = remnants_of_products
    print(temp)
    remnants_of_products = {}
    for key, value in temp.items():
        if value != Decimal(0):
            remnants_of_products[key] = value
    context = {'products':products, 'remnants_of_products':remnants_of_products, 'document_id':document_id,
               "document_date":document_date, 'date_to_filter_fireld':date_to_filter_fireld,
               'storage_field':storage_field}
    print(remnants_of_products)
    if request.POST.get('ajax'):
        template = get_template('documents_app/reports_remnants.html')
        return HttpResponse(template.render(context, request))
    return render(request, 'documents_app/base_report.html', context)


@login_required(login_url='users_app:login')
def get_day_income(request, date=date.today()):
    date = (request.POST['date']) if (request.POST.get('ajax')) else None
    products = ProductsInDocument.objects.filter(document__date=date)
    if request.POST.get('ajax'):
        print(request.POST)
        template = get_template('documents_app/table_report_day_income.html')
        return HttpResponse(template.render({'products':products, 'ajax':True}))
    context = {'products':products, 'ajax':False}
    return render(request, 'documents_app/report_day_income.html', context)


from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
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
    documents = Document.objects.all().order_by('-date')
    context = {'documents':documents}
    return render(request, 'documents_app/all_documents.html', context)


@login_required(login_url='users_app:login')
def detail_document(request, document_id = None):
    start=(datetime.now())
    if document_id != None:
        document = Document.objects.get(id=document_id)
        dishes = DishInDocument.objects.filter(document_id=document_id) if document.document_type == '1' else None
        dishesInDocument = [[dish, dish.id] for dish in dishes] if document.document_type == '1' else None
        products = ProductsInDocument.objects.filter(document_id=document_id) if document.document_type != '1' else None
        productsInDocument = [[product,product.id, product.data.get_unit_display]
                              for product in products] if document.document_type != '1' else None
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
        for i in moves:
            print(i.__str__())
        print(moves, request.POST)
        if request.POST['document_type'] != '1':
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

    context = {'form': form,
               'document_id': document_id,
               'products': products,
               'dishes': dishes,
               'document_type': 'dish' if (len(dishesInDocument) if dishesInDocument != None else False) != 0 else 'product',
               'productsInDocument': productsInDocument if productsInDocument or productsInDocument == None else None,
               'dishesInDocument': dishesInDocument
               }
    if document_id == None:
        context.update({'new': True})
    print(datetime.now() - start)
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
        return HttpResponse(template.render({'datas': dishInDocument, 'one_line':True, 'document_id':new_entry.document.id,
                                             'document_type':'dish'}, request))
    else:
        dishes = Dish.objects.all()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'add_dish':True, 'dishes':dishes,
                                             'url':'/documents/get_all_dishes_to_document/'}, request))


@login_required(login_url='users_app:login')
def delete_entry_from_document(request, entry_id, document_id, document_type=None):
    if document_type == 'dish':
        dish = DishInDocument.objects.get(id=entry_id)
        dish.delete()
    elif document_type == 'product':
        documents = ProductsInDocument.objects.get(id=entry_id)
        documents.delete()
    return HttpResponseRedirect(reverse('documents_app:detail_document', args=[document_id]))


@login_required(login_url='users_app:login')
def delete_document(request, document_id):
    document = Document.objects.get(id=document_id)
    document.delete()
    return HttpResponseRedirect(reverse('documents_app:all_documents'))

@login_required(login_url='users_app:login')
def get_all_products_to_document(request):
    if request.POST.get('object_id'):
        print('its this')
        new_entry = ProductsInDocument()
        new_entry.data = Product.objects.get(id=request.POST['object_id'])
        new_entry.document = Document.objects.get(id=request.POST['document_id'])
        new_entry.count = request.POST['count'].replace(',', '.')
        new_entry.save()
        productInDocument = [ProductInDocumentsForm(instance=new_entry), new_entry.id, new_entry.data.get_unit_display]
        template = get_template('documents_app/detail_document_product_or_dish.html')
        product_movement_dish(DishInDocument.objects.filter(document_id=new_entry.document.id))
        return HttpResponse(template.render({'datas': productInDocument, 'one_line': True,
                                             'document_id':new_entry.document.id, 'document_type':'product'}, request))
    elif request.POST.get('ajax'):
        print('docu,ent detail')
        product = Product()
        product.name = request.POST['name']
        product.unit = request.POST['unit']
        product.category = ProductCategory.objects.get(id=request.POST['category'])
        product.save()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'dish': product, 'line_number': request.POST['line_number'],
                                             'document_type':'product',
                                             'url': '/documents/get_all_products_to_document/'}, request))
    else:
        products = Product.objects.all()
        template = get_template('documents_app/all_dishes_to_document.html')
        return HttpResponse(template.render({'add_product':True, 'dishes':products, 'product':True,
                                             'url':'/documents/get_all_products_to_document/'}, request))


@login_required(login_url='users_app:login')
def products_remnants(request, document_id = None, document_date = date.today().strftime('%Y-%m-%d')):
    start = datetime.now()
    if request.GET.get('product_id'):
        product_id = request.GET['product_id']
    else:
        product_id=False
    document_date = document_date.split('.')
    document_date.reverse()
    document_date = '-'.join(document_date)
    date_to_filter_fireld = document_date
    print(document_date, product_id)
    storage_field = DocumentForm()
    movement_entries = MovingProducts.objects.filter(date__lte=document_date)
    if not product_id:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(id=product_id)
    remnants_of_products = {}
    for product in products:
        product_id_inloop = product.id
        for product_entry in movement_entries:
            product_count = product_entry.count
            if (product_entry.document.document_type in ['1', '2', '3']):
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
    #print(remnants_of_products)
    if request.POST.get('ajax'):
        template = get_template('documents_app/reports_remnants.html')
        print(datetime.now() - start)
        return HttpResponse(template.render(context, request))
    elif request.GET.get('ajax') and product_id:
        print(product_id)
        print(datetime.now() - start)
        return JsonResponse(remnants_of_products)
    print(datetime.now()-start)
    return render(request, 'documents_app/base_report.html', context)


@login_required(login_url='users_app:login')
def get_day_income(request, date=date.today()):
    date = (request.POST['date']) if (request.POST.get('ajax')) else None
    products = ProductsInDocument.objects.filter(document__date=date, document__document_type__exact='0')
    if request.POST.get('ajax'):
        print(request.POST)
        template = get_template('documents_app/table_report_day_income.html')
        return HttpResponse(template.render({'products':products, 'ajax':True}))
    context = {'products':products, 'ajax':False}
    return render(request, 'documents_app/report_day_income.html', context)


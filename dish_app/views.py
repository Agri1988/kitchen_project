from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse

from .models import Dish, Ingredients, Product, ProductCategory
from .forms import DishForm, ProductForm

# Create your views here.
@login_required(login_url='users_app:login')
def all_dishes(request):
    dishes = Dish.objects.all()
    context = {'dishes':dishes}
    return render(request, 'dish_app/all_dishes.html', context)


@login_required(login_url='users_app:login')
def detail_dish(request, dish_id = None):
    print(dish_id)
    if dish_id != None:
        dish = Dish.objects.get(id=dish_id)
        ingredients = Ingredients.objects.filter(dish=dish_id)
    else:
        dish = None
        ingredients = None
    if request.method != 'POST':
        form = DishForm(instance=dish)
    else:
        form = DishForm(instance=dish, data=request.POST)
        if form.is_valid():
            if dish_id == None:
                new_dish = form.save()
                new_id = new_dish.id
                print(new_id)
                return HttpResponseRedirect(reverse('dish_app:detail_dish', args=[new_id]))
            form.save()

    context = {'form': form, 'dish_id': dish_id, 'ingredients': ingredients}
    if dish_id == None:
        context.update({'new': True})

    return render(request, 'dish_app/detail_dish.html', context)


@login_required(login_url='users_app:login')
def all_products(request):
    def get_data():
        products = Product.objects.all()
        context = {'products': products}
        return context
    if request.GET.get('modal'):
        if request.GET['modal'] == 'True':
            template = get_template('dish_app/all_products_toDish.html')
            return HttpResponse(template.render(get_data(), request))

    return render(request, 'dish_app/all_products.html', get_data())


@login_required(login_url='users_app:login')
def add_product_to_dish(request):
    print(request.POST)
    dish = Dish.objects.get(id=request.POST['dish_id'])
    product = Product.objects.get(id=request.POST['product_id'])
    new_ingredient = Ingredients()
    new_ingredient.dish = dish
    new_ingredient.product = product
    new_ingredient.quantity = request.POST['quantity']
    new_ingredient.save()
    context = {'ingredient': new_ingredient}
    template = get_template('dish_app/add_product_to_dish.html')
    return HttpResponse(template.render(context, request))
    #return JsonResponse({'data': get_data_to_calculate_payroll(employee, constants, payroll=payroll)[:3]})


@login_required(login_url='users_app:login')
def detail_product(request, product_id=None):
    if product_id != None:
        product = Product.objects.get(id=product_id)
    else:
        product = None
    if request.method != 'POST':
        form = ProductForm(instance=product)
    else:
        form = ProductForm(instance=product, data=request.POST)
        if request.POST.get('ajax'):
            new_product = Product()
            new_product.name = request.POST['name']
            new_product.unit = request.POST['unit']
            new_product.category = ProductCategory.objects.get(id=request.POST['category'])
            new_product.save()
            new_id = new_product.id
            context = {'product': new_product, 'line_number': request.POST['line_number'] if
                                                request.POST.get('line_number') else False}
            template = get_template('dish_app/add_product_to_products_list.html')
            return HttpResponse(template.render(context, request))
        if form.is_valid():
            if product_id == None:
                new_product = form.save()
                new_id = new_product.id
                print(new_id)
                return HttpResponseRedirect(reverse('dish_app:detail_product', args=[new_id]))


    context = {'form': form, 'product_id': product_id}
    print(request.GET.get('ajax'))

    return render(request, 'dish_app/detail_product.html', context)


@login_required(login_url='users_app:login')
def add_field_element(request, template, form, fieldname):
    print(request.GET)
    if request.method != 'POST':
        print('get')
        context = {'form': form()}
        template = get_template(template)
        return HttpResponse(template.render(context, request))
    else:
        print(request.POST)
        form = form(data=request.POST)
        if form.is_valid():
            print('valid')
            new_element = form.save()
            new_element_id = new_element.id
            new_element_name = getattr(new_element, fieldname)
            print(new_element_name)
        data_dict = {'new_element_id':new_element_id, 'new_element_name':new_element_name}
        return JsonResponse(data_dict)
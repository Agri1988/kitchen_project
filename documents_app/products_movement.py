from decimal import Decimal

from dish_app.models import Product
from documents_app.models import MovingProducts, Document, DishInDocument
from dish_app.models import Ingredients, Dish

def product_movement(request, moves, products, document):
    def save_product_in_moves(product, doc):
        new_entry_in_moves = MovingProducts()
        new_entry_in_moves.date = doc.date
        new_entry_in_moves.document = Document.objects.get(id=doc.id)
        new_entry_in_moves.product = Product.objects.get(id=product.data.id)
        new_entry_in_moves.count = product.count
        new_entry_in_moves.operation_status = True
        new_entry_in_moves.save()

    def save_product_in_moves_dict(product):
        new_entry_in_moves = MovingProducts()
        new_entry_in_moves.date = product['date']
        new_entry_in_moves.document = Document.objects.get(id=product['document'])
        new_entry_in_moves.product = Product.objects.get(id=product['product'])
        new_entry_in_moves.count = product['count']
        new_entry_in_moves.operation_status = True
        new_entry_in_moves.save()

    print(moves, products)
    if request.POST.get('document_status') == 'on':
        if len(moves) == 0:
            if request.POST['document_type'] == '1':
                for product in products.values():
                    save_product_in_moves_dict(product)
            else:
                for product in products:
                    save_product_in_moves(product, document)
        elif (len(moves) != 0) and (len(moves) != len(products)):
            move_product_list = [move.product.id for move in moves]
            print(move_product_list)
            if request.POST['document_type'] == '1':
                for product in products.values():
                    if product['product'] not in move_product_list:
                        # print(type(product.data.id), product.data.id)
                        save_product_in_moves_dict(product)
            else:
                for product in products:
                    if product.data.id not in move_product_list:
                        #print(type(product.data.id), product.data.id)
                        save_product_in_moves(product, document)
        elif len(moves) == len(products):
            if request.POST['document_type'] == '1':
                for product in products.values():
                    for move in moves:
                        if product['product'] == move.product.id:
                            if product['count'] != move.count:
                                move.count = product['count']
                                move.save(update_fields=['count'])
            for move in moves:
                move.operation_status = True
                move.save(update_fields=['operation_status'])
    elif request.POST.get('document_status') == None:
        if len(moves) != 0:
            for move in moves:
                move.delete()


def product_movement_dish(dishes):
    products ={}
    for i, dish in enumerate(dishes):
        ingredients = Ingredients.objects.filter(dish=dish.data.id)
        for ing in ingredients:
            j = ing.product.id
            if j not in products:
                products[j] = {}
                products[j]['date'] = dish.document.date
                products[j]['product'] = ing.product.id
                products[j]['document'] = dish.document.id
                products[j]['operation_status'] = dish.document.document_status
                products[j]['count'] = (dish.count) * (ing.quantity)
            else:
                products[j]['count'] += (dish.count) * (ing.quantity)
    return products
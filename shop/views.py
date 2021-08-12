from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.core.paginator import Paginator
# Create your views here.
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password, check_password


def index(request):

    products = Product.get_all_products()
    categorys = Category.get_all_categorys()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categorys'] = categorys

    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        products = products.filter(title__icontains=item_name)
    return render(request, 'shop/index.html', data)


def detail(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


def validateCustomer(customer):
    error_messenge = None
    if(not customer.first_name):
        error_messenge = "First Name Requires !!"
    elif len(customer.first_name) < 4:
        error_messenge = "First Name must be 4 char long or more"
    elif not customer.last_name:
        error_messenge = "Last Name Requires !!"
    elif len(customer.last_name) < 4:
        error_messenge = "Last Name must be 4 char long or more"
    elif not customer.phone:
        error_messenge = "Phone number Requires !!"
    elif len(customer.password) < 6:
        error_messenge = "Password Must be 6 char"
    elif len(customer.email) < 5:
        error_messenge = "Email must be 5 char long"
    elif customer.isExists():
        error_messenge = "Email Address Already Registerd.."
    return error_messenge


def registerUser(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('last_name')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')

    # validation

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email,
    }
    error_messenge = None

    customer = Customer(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        password=password)
    error_messenge = validateCustomer(customer)

    # saving
    if not error_messenge:
        print(first_name, last_name, phone,
              email, password)
        customer.password = make_password(customer.password)
        customer.register()
        # this is redirect any page like index
        return redirect('index')
    else:
        data = {
            'error': error_messenge,
            'values': value
        }
        return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')


# def index(request):
#     product_objects = Products.objects.all()

#     item_name = request.GET.get('item_name')
#     if item_name != '' and item_name is not None:
#         product_objects = product_objects.filter(title__icontains=item_name)

#     paginator = Paginator(product_objects, 140)
#     page = request.GET.get('page')
#     product_objects = paginator.get_page(page)
#     return render(request, 'shop/index.html', {'product_objects': product_objects})


# def detail(request, id):
#     product_object = Products.objects.get(id=id)
#     return render(request, 'shop/detail.html', {'product_object': product_object})

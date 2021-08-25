from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.core.paginator import Paginator
from django.views import View
# Create your views here.
from django.http import HttpResponse
import shop.views

from django.contrib.auth.hashers import make_password, check_password


class Index(View):
    def post(self, request):
        # from server it will get product_id
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('index')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
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
        print('you are: ', request.session.get('email'))

        item_name = request.GET.get('item_name')
        if item_name != '' and item_name is not None:
            products = products.filter(title__icontains=item_name)
        return render(request, 'shop/index.html', data)


def detail(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'signup.html')
#     else:
#         return registerUser(request)


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
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
        error_messenge = self.validateCustomer(customer)

        if not error_messenge:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('index')  # this is redirect any page like index

        else:
            data = {
                'error': error_messenge,
                'values': value
            }
            return render(request, 'signup.html', data)

    # saving

    def validateCustomer(self, customer):
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


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email

                return redirect('index')
            else:
                error_message = 'Email or Password invalid'

        else:
            error_message = 'Email or Password invalid'
        print(customer)
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')

#     else:


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

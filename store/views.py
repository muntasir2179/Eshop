from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Category, Customer

# Create your views here.


def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryId = request.GET.get('category')
    if categoryId:
        if categoryId == "-1":
            products = Product.get_all_products()
        else:
            products = Product.get_all_products_by_categoryId(
                category_id=categoryId)
    else:
        products = Product.get_all_products()
    data = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'index.html', context=data)


# validation of users inputs
def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "First Name Required."
    elif len(customer.first_name) < 4:
        error_message = "First Name must be 4 char long or more."
    elif not customer.last_name:
        error_message = "Last Name Required."
    elif len(customer.last_name) < 4:
        error_message = "Last Name must be 4 char long or more."
    elif not customer.phone:
        error_message = "Phone number required."
    elif len(customer.phone) < 11:
        error_message = "Phone number must be 11 char long."
    elif not customer.password:
        error_message = "Password required."
    elif len(customer.password) < 5:
        error_message = "Password must be 6 char long."
    elif not customer.email:
        error_message = "Email required."
    elif customer.isExists():
        error_message = "This email is already registered. Use another email to signup."

    return error_message


# This function will handle the POST request
def registerUser(request):
    # fetching data
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email,
    }

    customer = Customer(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        password=password
    )

    error_message = validateCustomer(customer)

    # saving data into the database
    if not error_message:
        # hashing the user entered password
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('index')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', context=data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)

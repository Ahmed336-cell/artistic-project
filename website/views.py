from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, UpdatePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def about_us(request):
    return render(request, 'about_us.html')

def login_user(request):
    # Checking if logging in 
    if request.method == "POST":

        # Getting username and password
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticating user
        user = authenticate(request, username = username, password = password)

        # Checking if authenticating is success 
        if user is not None:
            
            # Logging in 
            login(request, user)

            current_user = UserProfile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.database_add(product = key, quantity = value)

            # Displaying message 
            messages.success(request, "You have been logged in successfully!")

            # Redirect home
            return redirect('home')
        
        # If not success
        else: 

            # Displaying message
            messages.success(request, "An error occurred while logging in, please try again!")
            
            # Redirect home
            return redirect('login_user')

    return render(request, "login_user.html")

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')

def register_user(request):
    # Check if signing in
    if request.method == 'POST':

        # Create instance of SignUpForm
        form = SignUpForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Create a user 
            form.save()
            
            # Get username and password from cleaned data from form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:

                login(request, user)

                # If authentication is successful
                messages.success(request, "You have been signed up successfully")

                # Redirect home
                return redirect('update_info')
            
            else:
                messages.success(request, "Authentication failed. Please try again.")
 
    else:
        form = SignUpForm()
        return render(request, 'register_user.html', {'form':form})

    return render(request, 'register_user.html', {'form': form})


def product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        return render(request, "product.html", {'product': product})
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist...")
        return redirect('home')
    
    
"""
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name= foo)
        products = Product.objects.filter(category = category)
        return render(request, "category.html", {'products': products, 'category': category})
    except:
        messages.error(request, "There is no product with this category...")
        return redirect('home')

"""
def filter_products(request):
        
    products = Product.objects.all()

    category_name = request.GET.get('category')
    categories = Category.objects.all()
    if category_name:
        products = products.filter(category__name=category_name)

    return render(request, 'home.html', {'products': products, 'categories': categories})

def update_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)

        form = UpdateUserForm(request.POST or None, instance = user)
        if form.is_valid():
            form.save()
            login(request, user)
            messages.success(request, "Your profile has been updated...")
            return redirect('home')
        return render(request, "update_user.html", {'form':form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    

def update_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        if request.method == "POST":
            form = UpdatePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully changed!")
                login(request, user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')

        else:
            form = UpdatePasswordForm(user)
            return render(request, "update_password.html", {"form": form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__id = request.user.id)

        form = UserInfoForm(request.POST or None, instance = user)
        if form.is_valid():
            form.save()

            messages.success(request, "Your profile has been successfully updated...")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "Product you've searched for doesn't exist... Please try again.")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {"searched": searched})
    else:
        return render(request, "search.html", {})
def orders(request):
    """
    Display the orders page.
    Note: This just renders the template since orders are stored in localStorage.
    """
    return render(request, 'orders.html')

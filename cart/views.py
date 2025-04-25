from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from website.models import Product
from django.http import JsonResponse
from django import forms
from django.core.mail import send_mail

def cart_summary(request):
    # Get a cart
    cart = Cart(request)

    # Get a products' quantities
    quantities = cart.get_quantities

    # Get cart products
    cart_products = cart.get_cart_products

    # Get totals
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Get a cart
    cart = Cart(request)
    
    # If action is 'post'
    if request.POST.get('action') == 'post':

        # Get a product id
        product_id = int(request.POST.get('product_id'))

        # Get a product quantity 
        product_quantity = int(request.POST.get('product_qty'))

        # Get a product 
        product = get_object_or_404(Product, id = product_id)
        
        # Save to a session
        cart.add(product = product, quantity = product_quantity)

        # Get cart quantity 
        cart_quantity = cart.__len__()

        messages.success(request, "Product has been successfully added to your cart...")
        # Get a response 
        response = JsonResponse({'quantity': cart_quantity})
        return response
        
        # Get a response 
        #response = JsonResponse({'Product name': product.name})
        
        # Return a response 
        #return response

def cart_delete(request):
    # If action is 'post'
    if request.POST.get('action') == 'post':
        try:
            # Get product id
            product_id = int(request.POST.get('product_id'))
            
            # Check if this is a clear all request
            clear_all = request.POST.get('clear_all', 'false').lower() == 'true'
            
            # Get the cart
            cart = Cart(request)
            
            # Delete the product
            cart.delete_product(product=product_id)
            
            # Return success response
            response = JsonResponse({'status': 'success', 'product': product_id})
            messages.success(request, "Product has been successfully removed from your cart.")
            return response
            
        except Exception as e:
            # Log the error for debugging
            print(f"Error in cart_delete: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def cart_update(request):
    # Get a cart
    cart = Cart(request)
    
    # If action is 'post'
    if request.POST.get('action') == 'post':

        # Get a product id
        product_id = int(request.POST.get('product_id'))

        # Get a product quantity 
        product_quantity = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_quantity)

        messages.success(request, "Quantity of the product has been successfully changed...")
        response = JsonResponse({'quantity': product_quantity})
        return response
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Here you would typically send an email
            # Uncomment and configure the following code when you have email settings configured
            '''
            send_mail(
                f'Contact Form: {subject}',
                f'Message from {name} ({email}):\n\n{message}',
                email,  # From email
                ['your-email@example.com'],  # To email
                fail_silently=False,
            )
            '''
            
            messages.success(request, 'Your message has been sent. Thank you!')
            return render(request, 'contact_us.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})


from django.http import HttpResponse
from django.shortcuts import render
from .models import *

def index(request):
    products=['Match Attax', '$2 per pack', '10 cards in a pack']
    return render(request, 'index.html', {'products':products})

def all_product(request):
    products=Product.objects.all()
    return render(request, 'products.html', {'products':products})

def product_individual(request, prodid):
    product = Product.objects.get(id=prodid)
    return render(request, 'product.html', {'product':product})

def individual_product(request, prodid):
    product = Product.objects.get(id=prodid)
    return render(request, 'individual_product.html', {'product':product})

from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import * 

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
    
from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")

from django.contrib.auth.decorators import login_required

@login_required
def add_to_basket(request, prodid):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(user_id=user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    product = Product.objects.get(id=prodid)
    sbi=BasketItem.objects.filter(basket_id=basket, product_id=product).first()
    if sbi is None:
        sbi = BasketItem(basket_id=basket, product_id=product)
        sbi.save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")

# views.py
@login_required
def show_basket(request):
    # get the user object
    # does a shopping basket exist ? -> your basket is empty
    # load all shopping basket items
    # display on page 
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        #TODO: Show basket empty
        return render(request, 'basket.html', {'empty':True})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        # is this list empty ? 
        if sbi.exists():
            # normal flow
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'basket.html', {'empty':True})
        
@login_required
def remove_item(request,sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket") # if error redirect to shopping basket
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity-1
            basketitem.save() # save our changes to the db
        else:
            basketitem.delete() # delete the basket item
    return redirect("/basket")

@login_required
def order(request):
    # load in all data we need, user, basket, items
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists(): # if there are no items
        return redirect("/")
    # POST or GET
    if request.method == "POST":
        # check if valid
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            for item in sbi:
                total += float(item.item_price())
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    else:
        # show the form
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    
@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})

def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})
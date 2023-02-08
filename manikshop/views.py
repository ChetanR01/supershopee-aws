import datetime
from traceback import print_tb
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.template.loader import render_to_string, get_template
from django.db.models import Q
from django.shortcuts import render
from .models import SubCategory, Category, Extended_user,Deal, Subscription, Cart, Order, Contact_form ,ProductDetails
from django.http import HttpResponse
import json

# for Payment Gateway 
from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')

# for base file
def get_subcategory(request):
    id = request.GET.get('id', '')
    result = list(SubCategory.objects.filter(category_id=int(id)).values('id', 'name'))
    return HttpResponse(json.dumps(result), content_type="application/json")


# Create your views here.
def index(request):
    products = ProductDetails.objects.all()
    deals = Deal.objects.filter(end_date__gte=datetime.datetime.now())
    categories= Category.objects.all()
    return render(request, "index.html", {"categories":categories,"products":products,"deals":deals})

def product(request):
    deals = Deal.objects.all()
    products = ProductDetails.objects.all().order_by("name")

    p = Paginator(products, 21)
    page_no= request.GET.get('page')

    try:
        page_obj = p.get_page(page_no)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    if len(page_obj) <= 3:
        no_col= 1
    elif len(page_obj) <= 6:
        no_col= 2
    elif len(page_obj) <= 9:
        no_col= 3
    elif len(page_obj) <= 12:
        no_col= 4
    elif len(page_obj) <= 15:
        no_col= 5
    elif len(page_obj) <= 18:
        no_col= 6
    elif len(page_obj) <= 21:
        no_col= 7
    return render(request, "product.html", {"products":page_obj,"no_col":no_col,"deals":deals})

def deal_product(request,id):
    deals = Deal.objects.all()
    deal_product = Deal.objects.get(id=id)
    products = deal_product.products.all().order_by("name")

    p = Paginator(products, 21)
    page_no= request.GET.get('page')

    try:
        page_obj = p.get_page(page_no)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    if len(page_obj) <= 3:
        no_col= 1
    elif len(page_obj) <= 6:
        no_col= 2
    elif len(page_obj) <= 9:
        no_col= 3
    elif len(page_obj) <= 12:
        no_col= 4
    elif len(page_obj) <= 15:
        no_col= 5
    elif len(page_obj) <= 18:
        no_col= 6
    elif len(page_obj) <= 21:
        no_col= 7
    return render(request, "deal-product.html", {"products":page_obj,"no_col":no_col,"deals":deals,"deal_product":deal_product})

def single(request, id):
    product = ProductDetails.objects.filter(id=id)
    for rel_pro in product:
        rel_category = rel_pro.category
    related_products = ProductDetails.objects.filter(category=rel_category)
    return render(request, "single.html", {"products":product,"related_products":related_products})

def default_search(request):
    deals = Deal.objects.all()
    if request.method == "GET":
        search_for =  request.GET.get('search')
        products = ProductDetails.objects.filter(Q(name__icontains=search_for)| Q(product_details__icontains=search_for)).order_by("name")
    
    p = Paginator(products, 21)
    page_no= request.GET.get('page')

    try:
        page_obj = p.get_page(page_no)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    if len(page_obj) <= 3:
        no_col= 1
    elif len(page_obj) <= 6:
        no_col= 2
    elif len(page_obj) <= 9:
        no_col= 3
    elif len(page_obj) <= 12:
        no_col= 4
    elif len(page_obj) <= 15:
        no_col= 5
    elif len(page_obj) <= 18:
        no_col= 6
    elif len(page_obj) <= 21:
        no_col= 7
    return render(request, "search.html", {"products":page_obj,"no_col":no_col,"deals":deals,"search_for":search_for})


def search(request,search_type,id):
    deals = Deal.objects.all()
    if search_type =="category":
        products = ProductDetails.objects.filter(category=id).order_by("name")

        p = Paginator(products, 21)
        page_no= request.GET.get('page')

        try:
            page_obj = p.get_page(page_no)
        except PageNotAnInteger:
            page_obj=p.page(1)
        except EmptyPage:
            page_obj=p.page(p.num_pages)


        if len(page_obj) <= 3:
            no_col= 1
        elif len(page_obj) <= 6:
            no_col= 2
        elif len(page_obj) <= 9:
            no_col= 3
        elif len(page_obj) <= 12:
            no_col= 4
        elif len(page_obj) <= 15:
            no_col= 5
        elif len(page_obj) <= 18:
            no_col= 6
        elif len(page_obj) <= 21:
            no_col= 7
        return render(request, "search.html", {"products":page_obj,"no_col":no_col,"deals":deals})
    elif search_type =="subcategory":
        products = ProductDetails.objects.filter(subcategory=id).order_by("name")
        p = Paginator(products, 21)
        page_no= request.GET.get('page')

        try:
            page_obj = p.get_page(page_no)
        except PageNotAnInteger:
            page_obj=p.page(1)
        except EmptyPage:
            page_obj=p.page(p.num_pages)

        if len(page_obj) <= 3:
            no_col= 1
        elif len(page_obj) <= 6:
            no_col= 2
        elif len(page_obj) <= 9:
            no_col= 3
        elif len(page_obj) <= 12:
            no_col= 4
        elif len(page_obj) <= 15:
            no_col= 5
        elif len(page_obj) <= 18:
            no_col= 6
        elif len(page_obj) <= 21:
            no_col= 7
        return render(request, "search.html", {"products":page_obj,"no_col":no_col,"deals":deals})
        

# add item to cart
def add_cart(request,id):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                my_cart = Cart.objects.get(name=request.user)
                if my_cart:
                    my_cart.products.add(id)
                    messages.info(request,"Item Added to Cart")
                    my_cart.save()
            except:
                new_cart = Cart.objects.create(name=request.user)
                new_cart.products.add(id)
                messages.info(request,"Item Added to Cart")
                new_cart.save()
            current_url = request.POST.get('current_url')
            if current_url:
                return HttpResponseRedirect(current_url)
            else:
                current_url = request.POST.get('next')
                return HttpResponseRedirect(current_url)
        else:
            messages.info(request, "Please login before adding products to cart")
            current_url = request.POST.get('current_url')
            return HttpResponseRedirect(current_url)
            

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

# remove item from cart
def remove_cart(request,id):
    if request.user.is_authenticated:
        my_cart = Cart.objects.get(name=request.user)
        if my_cart:
            my_cart.products.remove(id)
            messages.info(request,"Item Removed from Cart")
            my_cart.save()
        return redirect("/cart")

# track order
def track_order(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            order_id = request.POST['order_id']
            orders = Order.objects.filter(order_id=order_id)
            for order in orders:
                one_order = order
            if orders:
                status = one_order.order_status
                messages.info(request, f"Your Order status is '{status}'")
            else:
                messages.info(request, f"No Order found for OrderID: {order_id}")
        return redirect("/")

# to create order item from cart
def create_order(request):
    # check address before order
    extended_user = Extended_user.objects.get(user=request.user.id)
    if extended_user.address == "Not Available" or None:
        messages.info(request,"Please add your address before Checkout")
        return redirect("/cart")
        
    if request.method== "POST":
        item_count = request.POST['item_count']
        product_dict = {}
        for i in range(1,int(item_count)+1):
            product_dict[f"product{i}"]= request.POST[f'product{i}']
            product_dict[f"quantity{i}"]= request.POST[f'quantity{i}']

        from itertools import islice
        values = product_dict.values()
        length_to_split =  [2 for i in range(len(values)//2)]
        Inputt = iter(values)
        Output = [list(islice(Inputt, elem)) for elem in length_to_split]
        # print("@@@@@@@@@#########",Output)
        
        for rec in Output:
            product = ProductDetails.objects.get(id=int(rec[0]))
            create_order = Order.objects.create(cutomer_name=request.user, date= datetime.datetime.now(), product= product, quantity= int(rec[1]))
            create_order.save()
            
        if Output:        
            return redirect(f"/checkout/{create_order.order_id}")
        else:
            messages.info(request, "Your Cart🛒 is Empty!  Please add products to cart🛒")        
            return redirect("/cart")
    return redirect("/cart")

    # Checkout Order
def checkout(request,id):
    orders= Order.objects.filter(order_id=id)
    grand_total=0
    for order in orders:
        grand_total+=order.total_cost
    if grand_total<10:
        messages.info(request,"For checkout Order Value must be more than Rs.10, Please add more products to cart")
        return redirect("/cart")
    # create payment request
    response = api.payment_request_create(amount=grand_total,purpose=f"Transaction for Order ID: {id}",buyer_name=request.user.first_name,email=request.user.email,redirect_url="https://store.crrathod.tech/update-payment-status" )
    # print("Response : ",response)
    payment_order_id = response['payment_request']['id']
    for order in orders:
        order.payment_order_id=payment_order_id
        order.save()
    payment_url= response['payment_request']['longurl']
    # print(payment_url)

    return render(request, "checkout.html", {"orders":orders,"grand_total":grand_total,"order_id":id,"payment_url":payment_url})


    # Order History
def order_history(request):
    orders= Order.objects.filter(cutomer_name=request.user.id).order_by('-date')
    return render(request, "order_history.html", {"orders":orders})

# Update Payment Status
def update_payment_status(request):
    payment_order_id= request.GET.get('payment_request_id')
    transaction_id= request.GET.get('payment_id')
    payment_status= request.GET.get('payment_status')
    orders= Order.objects.filter(payment_order_id=payment_order_id)
    order_id = 0
    if payment_status=="Credit":
        product_list=[]
        for order in orders:
            order.transaction_id=transaction_id
            order.order_status="confirm"
            order.payment_method="prepaid"
            order.payment_status="confirm"
            order_id=order.order_id
            order.save()
            product_list.append(order.product.id)
        # Remove items from cart
        my_cart = Cart.objects.get(name=request.user)
        if my_cart:
            for product_id in product_list:
                my_cart.products.remove(product_id)
        my_cart.save()    
        return redirect(f"/confirm-order/online/{order_id}")
    else:
        for order in orders:
            order_id=order.order_id
        messages.info(request,"Payment Failed!, Please try again")
        return redirect(f"/checkout/{order_id}")

    # confirm Order
def confirm_order(request,mode,id):
    orders= Order.objects.filter(order_id=id)
    product_list=[]
    if mode=="cod":
        for order in orders:
            order.order_status="confirm"
            order.transaction_id="Not Applicable"
            order.save()
            product_list.append(order.product.id)
        messages.info(request, f"Your Order(Order Id:{id}) is Confirm")
        # return redirect("/")
            
    elif mode=="online":
        messages.info(request, f"Payment Recived Successfully, Thank You!")
    else: 
        print("Something went wrong")
        # return redirect("/cart")
    # remove item from cart
    my_cart = Cart.objects.get(name=request.user)
    if my_cart:
        for product_id in product_list:
            my_cart.products.remove(product_id)
    my_cart.save()

    return redirect(f"/checkout/{id}")


from manikshop.utils import render_to_pdf


def generate_report(request,order_id):
    template_name = "invoice_format.html"
    user=User.objects.get(id=request.user.id)
    orders = Order.objects.filter(order_id=order_id)
    grand_total=0
    for order in orders:
        grand_total+=order.total_cost
        rep_order=order

    return render_to_pdf(
        template_name,
        {
            "user":user,
            "rep_order":rep_order,
            "order_id":order_id,
            "orders": orders,
            "grand_total":grand_total,

            
        },
    )


def about(request):
    return render(request, "about.html", {})

def contact(request):
    return render(request, "contact.html", {})

def contact_form(request):
    if request.method== "POST":
        name = request.POST['name']
        subject = request.POST['subject']
        mobile_no = request.POST['mobile_no']
        email = request.POST['email']
        msg = request.POST['message']
        contact = Contact_form.objects.create(name=name,subject=subject,mobile_no=mobile_no,email=email,message=msg)
        contact.save()
        messages.info(request, "Thank You for Contacting Us, We'll get back to you shortly")

    return redirect("/")

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(name=request.user.id)
        return render(request, "cart.html", {"cart":cart})
    else:
        messages.info(request, "Please login to check your cart")
        return render(request, "cart.html", {})

def faqs(request):
    return render(request, "faqs.html", {})

def terms(request):
    return render(request, "terms.html", {})

def payment(request):
    return render(request, "payment.html", {})

def privacy(request):
    return render(request, "privacy.html", {})

def signup(request):
    if request.method== "POST":
        name = request.POST['name']
        mobile_no = request.POST['mobile_no']
        email = request.POST['email']
        username = request.POST['mobile_no'] # username = mobile_no
        password = request.POST['password']
        confirm_pass = request.POST['confirm_pass']

        
        if password == confirm_pass:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is Already Used!")
                return redirect('/')
            else:
                user = User.objects.create_user(username=username,password= password, email=email, first_name=name)
                user.save()
                extended_user=Extended_user.objects.create(user=user,mobile_no=mobile_no,user_type="customer", address="Not Available")
                extended_user.save()
                messages.info(request,"Your have successfully created account, Login Now!")

                return redirect('/')

        else:
            messages.info(request,"Password Not matching!")
            return redirect('/')

    else:
        return render(request, "/")

def login(request):
    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print(f"User {username} is loged in")
            messages.info(request,"You are successfully Loged In")
            return redirect("/")
        else:
            messages.info(request,"Invalid Credentials!")
            print("Invalid Login detaisl")
            return redirect("/")

    else:
        return render(request, "/")

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/")

def profile(request):
    if request.method== "POST":
        if request.user.is_authenticated:
            predata = User.objects.get(id=request.user.id)
            name = request.POST['name']
            email = request.POST['email']
            mobile_no = request.POST['mobile_no']
            address = request.POST['address']
            predata.first_name = name
            predata.email = email
            predata.username = mobile_no

            try:
                data_check =  Extended_user.objects.get(user = predata)
                print("data checker", data_check)
            except:
                data_check = False
            # if mobile no. or photo already uploaded
            if data_check:
                try:
                    data_check.address = address
                    data_check.mobile_no = mobile_no
                    
                except:
                    data_check.address= address
                    data_check.mobile_no = mobile_no
                data_check.save()
            else:                   
                ext_data = Extended_user(user=predata, mobile_no = mobile_no, address= address)                   
                ext_data.save()
                    
            predata.save()   
            messages.info(request,"Your account details successfully updated")
            return redirect('/')
        else:
            messages.info(request,"Please login to check/update your profile")
            return redirect('/')

    return render(request, "index.html")


def update_address(request):
    if request.method== "POST":
        if request.user.is_authenticated:
            predata = User.objects.get(id=request.user.id)
            name = request.POST['name']
            mobile_no = request.POST['mobile_no']
            address = request.POST['address']
            predata.first_name = name
            predata.username = mobile_no
            try:
                data_check =  Extended_user.objects.get(user = predata)
            except:
                data_check = False
            # if mobile no. or photo already uploaded
            if data_check:
                try:
                    data_check.address = address
                    data_check.mobile_no = mobile_no
                except:
                    data_check.address= address
                    data_check.mobile_no = mobile_no
                data_check.save()
            else:
                ext_data = Extended_user(user=predata, mobile_no = mobile_no, address= address)  
                ext_data.save()
            predata.save()   

            messages.info(request,"Your address successfully updated")
            return redirect('/cart')
        else:
            messages.info(request,"Please login to check/update your profile")
            return redirect('/cart')

    return render(request, "index.html")


def subscription(request):
    if request.method== "POST":
        if request.user.is_authenticated:
            predata = User.objects.get(id=request.user.id)
            name= predata.first_name
        else:
            temp_name = request.POST['email']
            name = temp_name.split('@')[0]
        email = request.POST['email']
        sub_data = Subscription(name=name, email = email, date= datetime.date.today())
        sub_data.save()
        messages.info(request,"Your Email is added to our subscribers list, Thank You!")
        
        return redirect("/")
    return redirect("/")


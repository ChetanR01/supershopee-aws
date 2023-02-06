from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta,date
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, auth
from manikshop.models import ProductDetails, Category, SubCategory,Order,Contact_form,Subscription,Deal,Extended_user

from .forms import ProductForm, DealsForm

def index(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            orders = Order.objects.all().order_by("-date")
            # for Order-Status (Pie Chart)
            orders_by_orders_ids = Order.objects.filter(date__gte=datetime.now()-timedelta(days=2)).order_by("order_id")
            pending_orders=0
            confirm_orders=0
            on_the_way_orders=0
            delivered_orders=0
            cancel_orders=0
            pre_id=0
            for order in orders_by_orders_ids:
                if order.order_id==pre_id:
                    pass
                else:
                    pre_id=order.order_id
                    if order.order_status=="pending":
                        pending_orders+=1
                    elif order.order_status=="cancelled":
                        cancel_orders+=1
                    elif order.order_status=="confirm":
                        confirm_orders+=1
                    elif order.order_status=="on_the_way":
                        on_the_way_orders+=1
                    elif order.order_status=="delivered":
                        delivered_orders+=1

            # for Order-Status (Bar Chart)
            categories =Category.objects.all()
            from django.db.models import Count
            result = (Order.objects.values('product__category').annotate(product_count=Count('product__category')).order_by('product__category'))

            category_id_list=[]
            temp_val_list=[]
            for rec in result:
                temp_val_list.append(rec['product_count'])
                category_id_list.append(rec['product__category'])

            values_list=[]
            temp_count=0
            for category in categories:
                if category.id in category_id_list:
                    values_list.append(temp_val_list[temp_count])
                    temp_count+=1
                else:
                    values_list.append(0)  

            # for Line Chart
            cod_orders_10days=[]
            prepaid_orders_10days=[]
            for i in range(10):
                _10days_orders_orderby_orders_ids = Order.objects.filter(date__gte=date.today()-timedelta(days=i),date__lt=date.today()-timedelta(days=i-1)).order_by("order_id")
                
                cod_orders=0
                prepaid_orders=0
                pre_id=0
                for order in _10days_orders_orderby_orders_ids:
                    if order.order_id==pre_id:
                        pass
                    else:
                        pre_id=order.order_id
                        if order.payment_method=="cash":
                            cod_orders+=1
                        elif order.payment_method=="prepaid":
                            prepaid_orders+=1

                cod_orders_10days.append(cod_orders)
                prepaid_orders_10days.append(prepaid_orders)

            # reverse prepaid_orders_10days and cod_orders_10days lists
            cod_orders_10days.reverse()
            prepaid_orders_10days.reverse()

            # Data Month format list i.e. 03/Feb,..
            temp_pre_10days_list= [datetime.now().date()-timedelta(days=i) for i in range(10)]
            pre_10days_list=[]            
            for i in temp_pre_10days_list:
                day=i.day
                if i.month==1:
                    month="Jan"
                if i.month==2:
                    month="Feb"
                if i.month==3:
                    month="Mar"
                if i.month==4:
                    month="Apil"
                if i.month==5:
                    month="May"
                if i.month==6:
                    month="June"
                if i.month==7:
                    month="Jul"
                if i.month==8:
                    month="Aug"
                if i.month==9:
                    month="Sept"
                if i.month==10:
                    month="Oct"
                if i.month==11:
                    month="Nov"
                else:
                    month="Dec"
                pre_10days_list.append(f"{day}{month}")
            pre_10days_list.reverse()

            return render(request, "01-index.html", {"orders":orders,"pending_orders":pending_orders,"cancel_orders":cancel_orders,"confirm_orders":confirm_orders,"on_the_way_orders":on_the_way_orders,"delivered_orders":delivered_orders,"categories":categories,"values_list":values_list,"pre_10days_list":pre_10days_list,"cod_orders_10days":cod_orders_10days,"prepaid_orders_10days":prepaid_orders_10days})
        else:
            messages.info(request,"You're not authorized to access this page, Please Contact Developer for Help!")
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

def orders(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            orders = Order.objects.all().order_by("-date")
            return render(request, "01-orders.html", {"orders":orders,})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")
    

def create_order(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            orders = Order.objects.all().order_by("-date")
            return render(request, "01-create-order.html", {"orders":orders,})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")
    

def update_order(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            orders = Order.objects.filter(order_id=id)
            if request.method=="POST":
                order_status = request.POST.get('order_status')
                payment_status = request.POST.get('payment_status')

                for order in orders:
                    order.order_status=order_status
                    order.payment_status=payment_status
                    order.save()
                messages.info(request,f"Order ({id}) Updated Successfully!")
                return redirect("/dashboard/orders")
            grand_total=0
            for order in orders:
                rep_order=order
                grand_total+=order.total_cost
            return render(request, "01-update-order.html", {"orders":orders,"rep_order":rep_order,"grand_total":grand_total})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")    

def product(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            products = ProductDetails.objects.all()
            raw_id=1
            for product in products:
                raw_id = product.id
            categories = Category.objects.all()
            return render(request, "01-products.html", {"products":products,"categories":categories,"raw_id":raw_id})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

# Add new product
def add_product(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            if request.method == "POST":
                form = ProductForm(id,request.POST or None, request.FILES or None)
                if form.is_valid():
                    category_id = request.POST.get('category')
                    subcategory_id = request.POST.get('subcategory')
                    category= Category.objects.get(id=int(category_id))
                    subcategory= SubCategory.objects.get(id=int(subcategory_id))
                    form.category = category
                    form.subcategory = subcategory
                    form.save()
                    return redirect("/dashboard/products")
                else:
                    print("ERROR !!! Unable to validate form ")
                    return render(f"/dashboard/add-product/{id}")

            form = ProductForm(p_id=id)
            categories=Category.objects.all()
            subcategories=SubCategory.objects.all()
            return render(request, "01-add-product.html", {"form":form,"categories":categories,"subcategories":subcategories})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    


# Edit Product
def edit_product(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            instance=ProductDetails.objects.get(id=id)
            if request.method == "POST":
                form = ProductForm(id,request.POST or None, request.FILES or None,instance=instance )
                if form.is_valid():
                    category_id = request.POST.get('category')
                    subcategory_id = request.POST.get('subcategory')
                    category= Category.objects.get(id=int(category_id))
                    subcategory= SubCategory.objects.get(id=int(subcategory_id))
                    form.category = category
                    form.subcategory = subcategory
                    form.save()
                    return redirect("/dashboard/products")
                else:
                    print("ERROR !!! Unable to validate form ")
                    return redirect(f"/dashboard/edit-product/{id}")

            form = ProductForm(p_id=id)
            print("Form Data = ",form.product.name)
            categories=Category.objects.all()
            subcategories=SubCategory.objects.all()
            return render(request, "01-edit-product.html", {"form":form,"categories":categories,"subcategories":subcategories})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    

# Add New Category
def add_category(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            if request.method == "POST":
                category_name = request.POST['new_category']
                category= Category.objects.create(name=category_name)
                category.save()
                return redirect("/dashboard/products")
            return redirect("/dashboard/products")
            
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    

# Deals
def deals(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            deals = Deal.objects.all()
            return render(request, "01-deals.html", {"deals":deals,})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login") 

# create new Deals
class DealCreateView(CreateView):
    # Unable to validate usertype for this page!!
    model = Deal
    form_class = DealsForm
    template_name = "01-create-deals.html"
    success_url = "/dashboard/deals"

# edit deals
def edit_deal(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            deal = Deal.objects.get(id=id)
            allproducts=ProductDetails.objects.all().order_by("id")
            if request.method =="POST":
                name = request.POST['name']
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                offer_line = request.POST['offer_line']
                banner = request.FILES['banner']
                deal.name =name
                deal.start_date =start_date
                deal.end_date =end_date
                deal.offer_line = offer_line
                deal.banner = banner

                for product in allproducts:
                    products= request.POST.get(f"products{product.id}")
                    if products:
                        deal.products.add(product.id)
                    else:
                        deal.products.remove(product.id)
                deal.save()
                return redirect("/dashboard/deals")

            return render(request, "01-edit-deal.html", {"deal":deal,"allproducts":allproducts})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    

# Support 
def contacts(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            contacts = Contact_form.objects.all().order_by("-date")
            return render(request, "01-contacts.html", {"contacts":contacts})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    
 
def view_contact(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            contact = Contact_form.objects.get(id=id)
            return render(request, "01-view-contact.html", {"contact":contact})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")
    

def subscribers(request):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            subscribers = Subscription.objects.all().order_by("-date")
            return render(request, "01-subscribers.html", {"subscribers":subscribers})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    

def login(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/dashboard")
        else:
            messages.info(request,"Invalid Credentials!")
            return redirect("/dashboard/login")
    return render(request, "01-login.html", {})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return render(request, "01-login.html", {})

# ACCOUNTs
# Choices are: cart, cust_name, date_joined, email, extended_user, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, password, user_permissions, username
def accounts(request,user_type):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            if user_type == "customer":
                users = User.objects.filter(is_staff=False)
                is_staff=False
            elif user_type == "employee":
                users = User.objects.filter(is_staff=True)
                is_staff=True
            return render(request, "01-accounts.html", {"users":users,"is_staff":is_staff})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")
    

# View User Account
def view_user(request,id):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            user = User.objects.get(id=id)
            return render(request, "01-view-user.html", {"user":user})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")
    

# Create New user
def create_user(request,user_type):
    if request.user.is_authenticated:
        try:
            data_check =  Extended_user.objects.get(user = request.user.id)
        except:
            data_check = False
        if data_check.user_type == "admin":
            if user_type == "customer":
                is_staff=False
            elif user_type == "employee":
                is_staff=True

            if request.method =="POST":
                name= request.POST['name']
                email= request.POST['email']
                mobile_no= request.POST['mobile_no']
                address= request.POST['address']
                username= request.POST['mobile_no']
                password= request.POST['password']
                confirm_password= request.POST['confirm_password']

                if is_staff:
                    username= request.POST['username']

                if password == confirm_password:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,"Username is Already Used!")
                        return redirect(f"/dashboard/create-user/{user_type}")
                    else:
                        user = User.objects.create_user(username=username,password= password, email=email, first_name=name,is_staff=is_staff)
                        user.save()
                        extended_user=Extended_user.objects.create(user=user,mobile_no=mobile_no,address=address,user_type=user_type)
                        extended_user.save()
                        messages.info(request,"Account Created!!")
                        return redirect(f"/dashboard/accounts/{user_type}")
                else:
                    messages.info(request,"Password Not matching!")
                    return redirect(f"/dashboard/create-user/{user_type}")

            return render(request, "01-create-user.html", {"is_staff":is_staff})
        else:
            return redirect("/dashboard/logout")
    else:
        return redirect("/dashboard/login")

    

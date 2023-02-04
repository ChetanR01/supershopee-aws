from datetime import date, datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# for rich text
from ckeditor.fields import RichTextField

# for category
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

# for Sub-category
class SubCategory(models.Model):
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
        

# For Product details
class ProductDetails(models.Model):
    name= models.CharField(max_length=100)
    price= models.FloatField()
    mrp= models.FloatField()
    main_img = models.ImageField(upload_to='product_img')
    img1 = models.ImageField(upload_to='product_img')
    img2 = models.ImageField(upload_to='product_img')
    img3 = models.ImageField(upload_to='product_img')
    category = models.ForeignKey(Category, related_name='produits', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='produits', on_delete=models.CASCADE)
    product_details = RichTextField(blank=True, null=True)
    trending = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


# For Order Table
class Order(models.Model):
    order_id = models.CharField(max_length=100, default="")
    cutomer_name = models.ForeignKey(User,  related_name='cust_name', on_delete=models.CASCADE)
    date = models.DateTimeField()
    address = models.CharField(max_length= 500)
    mobile_no = models.CharField(max_length = 12)
    product = models.ForeignKey(ProductDetails,  related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=1)
    total_cost = models.FloatField(default=1)
    order_state_list = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('confirm', 'Confirm'),
        ('on_the_way', 'On the way'),    
        ('delivered', 'Delivered'),    
        ]
    order_status = models.CharField(max_length=50, choices=order_state_list, default="pending")

    payment_state_list = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('confirm', 'Confirm') 
        ]
    payment_status = models.CharField(max_length=50, choices=payment_state_list, default="pending")

    payment_method_list = [
        ('cash', 'Cash On Delivery'),
        ('prepaid', 'Pre-Paid'), 
        ]
    payment_method = models.CharField(max_length=100, choices=payment_method_list, default="cash")
    payment_order_id = models.CharField(max_length=500)
    transaction_id = models.CharField(max_length=100)

    # Generate Order Id
    update_order_id = models.BooleanField(default=True)

    def get_order_id(self):
        today = datetime.now()
        date = today.strftime("%d")
        hrs = today.strftime("%H")
        min = today.strftime("%M")
        self.update_order_id=False 
        return f"{date}{today.month}{today.year}{hrs}{min}{self.cutomer_name.id}"

    # Get price
    def get_price(self):
        pro_id = ProductDetails.objects.get(id=self.product.id)
        return pro_id.price

    # Calculate total cost
    def cal_total(self):
        pro_id = ProductDetails.objects.get(id=self.product.id)
        return pro_id.price * self.quantity

    # Get Address
    def get_address(self):
        user = Extended_user.objects.get(user=self.cutomer_name.id)
        return user.address

    # Get Mobile No
    def get_mobile_no(self):
        user = Extended_user.objects.get(user=self.cutomer_name.id)
        return user.mobile_no

    def save(self, *args, **kwargs):
        if self.update_order_id:
            self.order_id = self.get_order_id()
        self.price = self.get_price()
        self.total_cost = self.cal_total()
        self.address = self.get_address()
        self.mobile_no = self.get_mobile_no()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id


# for Cart
class Cart(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    products= models.ManyToManyField(to=ProductDetails, related_name="cart", blank=True)

    def __str__(self):
        return self.name.first_name

# for Deals
class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    banner = models.ImageField(upload_to='deals')
    offer_line= models.CharField(max_length=300)
    products= models.ManyToManyField(to=ProductDetails, related_name="deals", blank=True)
    start_date= models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

# Extended user
class Extended_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=12)
    address = models.CharField(max_length=500)
    USER_TYPE = (('admin', "Admin"), ('employee', "Employee"), ('customer', "Customer"))
    user_type = models.CharField(choices=USER_TYPE, max_length=10, default="customer")

    def __str__(self):
        return self.user.first_name

# Subscription table
class Subscription(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    date = models.DateField()

    def __str__(self):
        return self.name

# Contact Forms
class Contact_form(models.Model):
    name = models.CharField(max_length=300)
    subject= models.CharField(max_length=500)
    mobile_no = models.CharField(max_length=12)
    email = models.CharField(max_length=200)
    message = models.TextField()
    date= models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return self.name
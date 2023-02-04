from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category,SubCategory,ProductDetails, Deal, Extended_user, Subscription, Order, Cart, Contact_form
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Category)
admin.site.register(Cart)
# admin.site.register(ProductDetails)
# admin.site.register(Deal)

# Extended user
class Extended_userInline(admin.StackedInline):
    model =Extended_user
    can_delete = False
    verbose_name_plural = 'Extended_Users' 

class CustomizedUserAdmin(UserAdmin):
    inlines = (Extended_userInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

# TO Modify SubCategory view for admin
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','category']
    # list_editable = ['verified']
admin.site.register(SubCategory, SubCategoryAdmin)

# TO Modify Product Detalis view for admin
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ['name','price','mrp','category','trending']
    list_editable = ['price','mrp','trending']
    search_fields = ('name', 'product_details')
    list_filter = ('category',)
admin.site.register(ProductDetails, ProductDetailsAdmin)

# TO Modify Order view for admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','date','product','quantity','total_cost','order_status']
    list_filter = ('order_id',)
    # list_editable = ['price','mrp','trending']
admin.site.register(Order, OrderAdmin)

# TO Modify Deals view for admin
class DealAdmin(admin.ModelAdmin):
    list_display = ['name','start_date','end_date']
    list_editable = ['start_date','end_date']
admin.site.register(Deal, DealAdmin)

# TO Modify Subscription view for admin
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name','email']
admin.site.register(Subscription, SubscriptionAdmin)


# Conatct form data
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name','date','subject']
admin.site.register(Contact_form, ContactFormAdmin)
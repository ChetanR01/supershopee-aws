from unicodedata import category
from .models import Category, SubCategory, Cart

def pass_cat_nd_sub_cat(request):
    all_categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(name=request.user.id)
            itemscount= cart.products.all().count()
        except:
            itemscount=0
    else:
        itemscount = 0

    return {"all_categories":all_categories, "sub_categories":sub_categories,"item_count":itemscount}
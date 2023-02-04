from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# from django.conf.urls import url
from . import views
app_name = 'admin_dashboard'

urlpatterns = [
    # re_path(r'^getSubcategory/$', views.get_subcategory),
    path('',views.index, name="index"),
    path('products/',views.product, name="products"),
    path('add-product/<int:id>',views.add_product, name="add-product"),
    path('edit-product/<int:id>',views.edit_product, name="edit-product"),
    path('add-category/',views.add_category, name="add-category"),

    path('orders/',views.orders, name="orders"),
    path('create-order/',views.create_order, name="create-order"),
    path('update-order/<str:id>',views.update_order, name="update-order"),

    path('deals/',views.deals, name="deals"),
    path('create-deals/',views.DealCreateView.as_view()),
    path('edit-deal/<int:id>',views.edit_deal, name="edit-deal"),


    path('contacts/',views.contacts, name="contacts"),
    path('view-contact/<int:id>',views.view_contact, name="view-contact"),
    path('subscribers/',views.subscribers, name="subscribers"),
    
    path('accounts/<str:user_type>',views.accounts, name="accounts"),
    path('view-user/<int:id>',views.view_user, name="view-user"),
    path('create-user/<str:user_type>',views.create_user, name="create-user"),

    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
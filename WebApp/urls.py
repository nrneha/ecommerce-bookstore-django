from django.urls import path
from WebApp import views

urlpatterns = [
    path('',views.Home_page,name="Home"),
    path('About/',views.About_page,name="About"),
    path('Contact/',views.Contact_page,name="Contact"),
    path('Products/',views.Product_page,name="Products"),
    path('Filter/<categ>/',views.Filter_Products,name="Filter"),
    path('CustomerSupport/',views.Save_Customer,name="CustomerSupport"),
    path('Single_Product/<int:b_id>',views.Single_Product,name="Single_Product"),
    path('user_login_page/',views.user_login_page,name="user_login_page"),
    path('Save_UserAccount/',views.Save_UserAccount,name="Save_UserAccount"),
    path('User_Login/',views.User_Login,name="User_Login"),
    path('User_Logout/',views.User_Logout,name="User_Logout"),
    path('save_cart/',views.save_cart,name="save_cart"),
    path('view_cart/',views.view_cart,name="view_cart"),
    path('remove_cartitem/<int:b_id>',views.remove_cartitem,name="remove_cartitem"),
    path('UserAccount_Reg/',views.UserAccount_Reg,name="UserAccount_Reg"),
    path('checkout_page/',views.checkout_page,name="checkout_page"),
    path('save_checkout_data/',views.save_checkout_data,name="save_checkout_data"),
    path('payment_page/',views.payment_page,name="payment_page"),
]
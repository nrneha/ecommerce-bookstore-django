from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Backend.models import BooksDB, CategoryDB
from WebApp.models import *
from django.contrib import messages
import razorpay
from django.contrib.auth.hashers import make_password,check_password
from .utils import user_login_required
from django.core.cache import cache



def Home_page(request):
    data = cache.get('all_category')
    print("from cacche",data)
    if data is None:
        data = list(CategoryDB.objects.all())
        cache.set('all_category',data,timeout=60*15)
        print("from db")
    return render(request, "Home.html", {'data': data})


def About_page(request):
    return render(request, "About.html")

def Contact_page(request):
    return render(request, "Contact.html")


def Product_page(request):
    books = cache.get('all_books')
    if books is None:
        books = list(BooksDB.objects.all())  # getting all products details
        cache.set('all_books',books,timeout=60*15) # set cache timeout 5 minutes for all products

    return render(request, "View_Products.html", {'books': books})


def Filter_Products(request, categ):

    cache_key = f'book_category_{categ}'
    books = cache.get(cache_key)
    if books is None:
        books = list(BooksDB.objects.filter(Category=categ))  # getting the products by the category
        cache.set(cache_key,books,timeout=60*15) # set cache timeout 5 minutes for books by category

    return render(request, "Filtered_Products.html", {'books': books, 'category': categ})


# saving the customer contact details and messages
def Save_Customer(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        sb = request.POST.get('subject')
        msg = request.POST.get('message')

        ob = CustomerDB(Name=nm, Email=em, Subject=sb, Message=msg)
        ob.save()
        return redirect(Contact_page)


def Single_Product(request, b_id):
    cache_key=f'single_book_{b_id}'
    book = cache.get(cache_key)
    if book is None:
        book = BooksDB.objects.get(id=b_id) # getting single product details by using the product id
        cache.set(cache_key,book,timeout=60*15) # set timeout for 5 minutes for a book

    return render(request, "Single_Product.html", {'book': book})


# registration form for new user
def UserAccount_Reg(request):
    return render(request, "UserRegistration.html")


def Save_UserAccount(request):
    # getting user registration details from the form
    if request.method == "POST":
        nm = request.POST.get('user')
        em = request.POST.get('email')
        ps = request.POST.get('password1')

        # save the user details to User_Account db
        obj = User_Accounts(Name=nm, Email=em, Password=make_password(ps))  # here user password stored as hashed
        obj.save()
        messages.success(request, "Success! Your account is now active.Please Login.. Happy shopping")
        return redirect(UserAccount_Reg)


def User_Login(request):
    if request.method == "POST":
        un = request.POST.get('user')
        ps = request.POST.get('password')

        try:
            user = User_Accounts.objects.get(Name=un)
            if check_password(ps,user.Password): # checking  plain text password and hashed password are same
                request.session['Name']=user.Name
                messages.success(request, "WELCOME.!")
                return redirect(Home_page)
            
            else:
                messages.error(request,"Incorrect Password")
                return redirect(UserAccount_Reg)
        except User_Accounts.DoesNotExist:
            messages.error(request,"User not found")
            return redirect(UserAccount_Reg)
        

def User_Logout(request):
    del request.session['Name'] # user logging out with deleting the session
    messages.success(request, "You have been signed out.")
    return redirect(Home_page)

@user_login_required
def save_cart(request):
    if request.method == "POST":
        un = request.POST.get('user')
        bn = request.POST.get('bookname')
        pc = request.POST.get('price')
        qt = request.POST.get('quantity')
        tp = request.POST.get('total')

        obj = CartDB(Customer=un, Book=bn, Price=pc, Quantity=qt, Total=tp)  # saving product details into cart db
        obj.save()
        messages.success(request, "Your book has been added to the cart..Great choice!!")
        return redirect(Product_page)



@user_login_required
def view_cart(request):
    data = CartDB.objects.filter(Customer=request.session['Name'])  # getting cart details with the user session names
    total = 0
    subtotal = 0
    delivery = 0
    for d in data:  # finding the subtotal and delivery charge with the carted products
        subtotal = subtotal + d.Total
        if subtotal >= 400:
            delivery = 50
        else:
            delivery = 120
        total = subtotal + delivery

    return render(request, "Cart.html", {'data': data, 'total': total, 'subtotal': subtotal, 'delivery': delivery})


@user_login_required
def remove_cartitem(request, b_id):
    x = CartDB.objects.get(id=b_id) # getting the product through id and deleting it
    x.delete()
    messages.success(request, "The book has been removed from your cart")
    return redirect(view_cart)


def user_login_page(request):
    return render(request, "UserLogin.html") # for viewing signin page

@user_login_required
def checkout_page(request):
    data = CartDB.objects.filter(Customer=request.session['Name'])
    total = 0
    subtotal = 0
    delivery = 0
    for d in data:
        subtotal = subtotal + d.Total
        if subtotal >= 400:
            delivery = 50
        else:
            delivery = 120
        total = subtotal + delivery
    return render(request, "CheckoutPage.html", {'subtotal': subtotal, 'delivery': delivery, 'total': total})

@user_login_required
def save_checkout_data(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        mb = request.POST.get('mobile')
        ad = request.POST.get('address')
        tt = request.POST.get('total')
        ob = CheckOutDB(Customer=nm, Email=em, Mobile=mb, Address=ad, Total=tt)
        ob.save()  # save checkout details in to checkout db
        return redirect(payment_page)

@user_login_required
def payment_page(request):
    customer = CheckOutDB.objects.order_by('-id').first()
    payy = customer.Total
    amount = int(payy * 100)
    pay_str = str(amount)
    for i in pay_str:
        print(i)
    if request.method == "POST":
        order_currency = "INR"
        client = razorpay.Client(auth=(''))
        payment = client.order.create({'amount': amount, 'currency': order_currency, 'payment_capture': '1'})
    return render(request, "payment.html", {'customer': customer, 'pay_str': pay_str})

@user_login_required
def account_delete_page(request):
    return render(request, "delete_account.html")

@user_login_required
def account_delete(request, user):
    cart = CartDB.objects.filter(Customer=user)
    cart.delete()
    del request.session['Name']
    del request.session['Password']
    data = User_Accounts.objects.get(Name=user)
    data.delete()  # deleting the account details from the db
    messages.success(request, "You have successfully deleted your account.")
    return redirect("Home")



@user_login_required
def customer_testimonials(request):# testimoial page shows users reviews about the books they read
    return render(request,"customer_testimonials.html")

@user_login_required
def write_review(request):# page for users to write the review of the books they read
    return render(request,"review_form.html")


def save_user_review(request,user):

    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        review = request.POST.get("review")

        review = UserReviews(book_title=book_title,review=review,user=user)
        review.save()
        messages.success(request,"Thank you for your review")
        return redirect(Home_page)

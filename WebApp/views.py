from django.shortcuts import render,redirect
from Backend.models import BooksDB,CategoryDB
from WebApp.models import CustomerDB,User_Accounts,CartDB,CheckOutDB
from django.contrib import messages
import razorpay

# Create your views here.

def Home_page(request):
    data = CategoryDB.objects.all()
    return render(request,"Home.html",{'data':data})

def About_page(request):
    return render(request,"About.html")

def Contact_page(request):
    return render(request,"Contact.html")

def Product_page(request):
    books = BooksDB.objects.all()
    return render(request,"View_Products.html",{'books':books})

def Filter_Products(request,categ):
    books = BooksDB.objects.filter(Category=categ)
    return render(request,"Filtered_Products.html",{'books':books,'category':categ})

def Save_Customer(request):
    if request.method=="POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        sb = request.POST.get('subject')
        msg = request.POST.get('message')

        ob = CustomerDB(Name =nm,Email=em, Subject=sb, Message =msg)
        ob.save()
        return redirect(Contact_page)

def Single_Product(request,b_id):
    book = BooksDB.objects.get(id=b_id)
    return render(request,"Single_Product.html",{'book':book})

def UserAccount_Reg(request):
    return render(request,"UserRegistration.html")

def Save_UserAccount(request):
    if request.method=="POST":
        nm = request.POST.get('user')
        em = request.POST.get('email')
        ps = request.POST.get('password1')
        # img = request.FILES['image']

        obj = User_Accounts( Name =nm,Email =em,Password =ps)
        obj.save()
        messages.success(request,"Success! Your account is now active.Please Login.. Happy shopping")
        return redirect(UserAccount_Reg)

def User_Login(request):
    if request.method=="POST":
        un = request.POST.get('user')
        ps = request.POST.get('password')
        request.session['Name']=un
        request.session['Password']=ps
        if User_Accounts.objects.filter(Name =un,Password =ps).exists():
            messages.success(request,"WELCOME.!")
            return redirect(Home_page)
        else:
            messages.error(request,"User not found.!")
            return redirect(UserAccount_Reg)
    else:
        return redirect(UserAccount_Reg)
def User_Logout(request):
    del request.session['Name']
    del request.session['Password']
    messages.success(request,"You have been signed out. Come back soon!")
    return redirect(Home_page)


def save_cart(request):
    if request.method=="POST":
        un = request.POST.get('user')
        bn = request.POST.get('bookname')
        pc = request.POST.get('price')
        qt = request.POST.get('quantity')
        tp = request.POST.get('total')

        obj = CartDB(Customer =un,Book =bn,Price =pc, Quantity = qt, Total =tp)
        obj.save()
        messages.success(request,"Your book has been added to the cart..Great choice!!")
        return redirect(Product_page)

def view_cart(request):
    data = CartDB.objects.filter(Customer=request.session['Name'])
    total = 0
    subtotal = 0
    delivery= 0
    for d in data:
        subtotal = subtotal+d.Total
        if subtotal>=400:
            delivery = 50
        else:
            delivery = 120
        total = subtotal + delivery

    return render(request,"Cart.html",{'data':data,'total':total,'subtotal':subtotal,'delivery':delivery})

def remove_cartitem(request,b_id):
    x = CartDB.objects.get(id=b_id)
    x.delete()
    messages.success(request,"The book has been removed from your cart")
    return redirect(view_cart)
def user_login_page(request):
    return render(request,"UserLogin.html")

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
    return render(request,"CheckoutPage.html",{'subtotal':subtotal,'delivery':delivery,'total':total})

def save_checkout_data(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        mb = request.POST.get('mobile')
        ad = request.POST.get('address')
        tt = request.POST.get('total')
        ob = CheckOutDB(Customer=nm,Email =em,Mobile =mb,Address =ad,Total=tt)
        ob.save()
        return redirect(payment_page)

def payment_page(request):
    customer = CheckOutDB.objects.order_by('-id').first()
    payy = customer.Total
    amount = int(payy*100)
    pay_str = str(amount)
    for i in pay_str:
        print(i)
    if request.method=="POST":
        order_currency = "INR"
        client = razorpay.Client(auth=('rzp_test_U0yRWmp89Hl5OI','mXkgiRPKZztlHvSqrXvKzDCu'))
        payment = client.order.create({'amount':amount,'currency':order_currency,'payment_capture':'1'})
    return render(request,"payment.html",{'customer':customer,'pay_str':pay_str})


def account_delete_page(request):
    return render(request,"delete_account.html")

def account_delete(request,user):
    cart = CartDB.objects.filter(Customer=user)
    cart.delete()
    del request.session['Name']
    del request.session['Password']
    data = User_Accounts.objects.get(Name=user)
    data.delete()
    messages.success(request,"You have successfully deleted your account.")
    return redirect("Home")




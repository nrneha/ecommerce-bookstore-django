from django.shortcuts import render,redirect
from Backend.models import CategoryDB,BooksDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from WebApp.models import CustomerDB
from django.contrib import messages
# Create your views here.

def View_IndexPage(request):
    return render(request,"index.html")

def Add_Categories(request):
    return render(request,"Add_Category.html")

def Save_Categories(request):
    if request.method=="POST":
        cnm = request.POST.get('category')
        cds = request.POST.get('description')
        img = request.FILES['image']

        obj = CategoryDB( category =cnm,Description =cds,Image = img)
        obj.save()
        messages.success(request,"Category Added Successfully.!")
        return redirect(Add_Categories)
def View_CategoryData(request):
    data = CategoryDB.objects.all
    return render(request,"View_Category.html",{'data':data})

def EditPage_Category(request,c_id):
    item = CategoryDB.objects.get(id=c_id)
    return render(request,"Edit_Category.html",{'item':item})

def Update_CategoryData(request,c_id):
    if request.method == "POST":
        cnm = request.POST.get('category')
        cds = request.POST.get('description')
        try:
            img = request.FILES['image']
            x = FileSystemStorage()
            file = x.save(img.name,img)
        except MultiValueDictKeyError:
            file = CategoryDB.objects.get(id=c_id).Image
        CategoryDB.objects.filter(id=c_id).update( category =cnm,Description =cds,Image = file)
        messages.success(request, "Updated Successfully.!")
        return redirect(View_CategoryData)


def Delete_CategoryData(request,c_id):
    data = CategoryDB.objects.get(id=c_id)
    data.delete()
    messages.info(request,"Category Deleted.!")
    return redirect(View_CategoryData)


def Add_BooksData(request):

    c_data = CategoryDB.objects.all()
    return render(request,"Add_Books.html",{'c_data':c_data})


def Save_BookDetails(request):
    if request.method=="POST":
        bnm = request.POST.get('name')
        bct = request.POST.get('category')
        bds = request.POST.get('description')
        bpr = request.POST.get('price')
        bim = request.FILES['image']

        ob = BooksDB(Name =bnm, Category =bct, Description =bds, Price =bpr,Image =bim)
        ob.save()
        messages.success(request,"New Book Added Successfully.!")
        return redirect(Add_BooksData)


def View_BookData(request):
    data = BooksDB.objects.all()
    return render(request,"Show_BOOKS.html",{'data':data})

def ViewPage_BookEdit(request,b_id):
    b_data = BooksDB.objects.get(id=b_id)
    c_data = CategoryDB.objects.all()
    return render(request,"EditPage.html",{'b_data':b_data,'c_data':c_data})

def Save_updations(request,b_id):
    if request.method=="POST":
        bnm = request.POST.get('name')
        bct = request.POST.get('category')
        bds = request.POST.get('description')
        bpr = request.POST.get('price')
        try:
            img = request.FILES['image']
            x = FileSystemStorage()
            file = x.save(img.name,img)
        except MultiValueDictKeyError:
            file = BooksDB.objects.get(id=b_id).Image
        BooksDB.objects.filter(id=b_id).update( Name =bnm, Category =bct, Description =bds, Price =bpr,Image =file)
        messages.success(request,"Updated Successfully.!")
        return redirect(View_BookData)

def Delete_Books(request,b_id):
    x = BooksDB.objects.get(id=b_id)
    x.delete()
    messages.info(request,"Book Deleted.!!")
    return redirect(View_BookData)





# Admin Login and Logout
def View_LoginPage(request):
    return render(request,"Admin_Login.html")

def Admin_login(request):
    if request.method=="POST":
        un = request.POST.get('username')
        ps = request.POST.get('password')

        if User.objects.filter(username__contains= un).exists():
            x = authenticate(username=un,password=ps)
            if x is not None:
                login(request,x)
                request.session['username']=un
                request.session['password']=ps
                messages.success(request,"Welcome!!")

                return redirect(View_IndexPage)
            else:
                messages.error(request,"Incorrect Password!!")

                return redirect(View_LoginPage)
        else:
            messages.error(request,"User not found")

            return redirect(View_LoginPage)


def Admin_Logout(request):
    del request.session['username']
    del request.session['password']
    messages.success(request,"Signed out Successfully.")
    return redirect(View_LoginPage)




# Customer Enquiry
def Customer_Support(request):
    data = CustomerDB.objects.all()
    return render(request,"CustomerSupport.html",{'data':data})

def CustomerDB_Delete(request,c_id):
    x = CustomerDB.objects.get(id=c_id)
    x.delete()
    return redirect(Customer_Support)

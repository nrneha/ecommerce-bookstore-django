from django.shortcuts import redirect
from WebApp.models import User_Accounts

def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        name = request.session.get('Name')
        if name and User_Accounts.objects.filter(Name=name).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_login_page')
    return wrapper

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        # else:
        #     return HttpResponse("You are not authenticated")    #create a page and send this msg, add redirect to login
        return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if(request.user.groups.exists()):
                group = request.user.groups.all()[0]
            if str(group) in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(group)
        return wrapper_func
    return decorator    

def admindecorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if(request.user.groups.exists()):
            group = request.user.groups.all()[0]
        if str(group) == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('logout')
            #return view_func(request, *args, **kwargs)
    return wrapper_func


def userdecorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if(request.user.groups.exists()):
            group = request.user.groups.all()[0]
        if str(group) == 'users':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
            #return view_func(request, *args, **kwargs)
    return wrapper_func


def vendordecorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if(request.user.groups.exists()):
            group = request.user.groups.all()[0]
        if str(group) == 'vendor':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
            #return view_func(request, *args, **kwargs)
    return wrapper_func


def useradmindecorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if(request.user.groups.exists()):
            group = request.user.groups.all()[0]
            print(group)
        if str(group) == 'users':
            return view_func(request, *args, **kwargs)
        if  str(group) == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
            #return view_func(request, *args, **kwargs)
    return wrapper_func
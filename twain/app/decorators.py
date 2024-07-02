from .models import *
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def buyer_role_required(func):
    def wrapper_func(request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        try:
            buyer=CostomerProfileModel.objects.get(user=user)
            return func(request,*args,**kwargs)
        except Exception:
            return redirect('index')
        
    return wrapper_func

def seller_role_required(func):
    def wrapper_func(request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        return func(request,*args,**kwargs) if user.is_dealer else redirect('index')
    return wrapper_func

def profile_required(func):
    def wrapper_func(request,*args,**kwargs):
        user=User.objects.get(id=request.user.id)
        if user.is_costomer:
            try:
                buyer=CostomerProfileModel.objects.get(user=user)
                return func(request,*args,**kwargs)
            except Exception:
                return redirect('buyeradd')
        elif user.is_dealer:
            try:
                seller=DealerProfileModel.objects.get(user=user)
                return func(request,*args,**kwargs)
            except Exception:
                return redirect('selleradd')
        else:
            return redirect('signup')
    return wrapper_func

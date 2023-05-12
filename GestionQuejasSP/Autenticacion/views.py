from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.

#class VRegistro(View):
  # def get (self,request):
  #      form=UserCreationForm()
 #       return render(request,"Autenticacion/login.html",{"form":form})


   # def post (self,request):
    #    pass

def logear(request):
    if(request.method=="POST"):
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            passw=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario,password=passw)
            if usuario is not None:
                login(request,usuario)
                return redirect('dash')
            else:
                messages.error(request,"usuario no valido")
        else:
            messages.error(request,"informacion incorrecta")
    form=AuthenticationForm()
    return render(request,"Autenticacion/login.html",{"form":form})

def cerrar_sesion(request):
    logout(request)
    return redirect('autenticacion')
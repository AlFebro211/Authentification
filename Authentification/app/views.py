from Authentification.settings import EMAIL_HOST_USER
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages as ms
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

def home  (request):
   return render (request, 'index.html')


def registrer (request):
    if request.method == "POST":
        username = request.POST ['username']
        firstname = request.POST ['firstname']
        lastname = request.POST ['lastname']
        email = request.POST ['email']
        password = request.POST ['password']
        confirm_motpass = request.POST ['confirm password']
        if User.objects.filter(username=username):
            ms.error(request,"ce nom a ete deja utilise")
            return redirect('registrer')
        
        if User.objects.filter(email=email):
            ms.error(request,'cet email a deja un compte')
            
        if not username.isalnum():
            ms.error(request,'le nom doit etre un alphanumeric')
            return redirect('registrer')
        if password != confirm_motpass:
            ms.error(request,'les deux mots de pass ne coincide pas')
            return redirect('registrer')
        mon_utilisateur = User.objects.create_user(username,email,password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname 
        mon_utilisateur.save()
        ms.success(request, "votre compte a ete cree avec succes" )
        subject = "bienvenu sur Febrox django system login"
        message = "bienvenue" + mon_utilisateur.first_name + "  " + mon_utilisateur.last_name + "\n Nous sommes heureux de vous recevoir\n\n\n merci\n\n FEBROX PRO"
        from_email = EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject,message,from_email, to_list,fail_silently=False)
        return redirect ('login')        
    return render(request,'register.html')

def logIn (request):
    if request.method == "POST":
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password = password)
        if user is not None:
            login(request,user)
            firstname = user.first_name
            ms.success (request,'felicitation!! vous avez ete connecte')
            return render(request,'index.html',{'firstname':firstname})
        else:
            ms.error(request,'Mauvaise authentification ')
            return redirect ('login')
    return render(request,'register.html')
    
def logOut(request):
    logout(request)
    ms.success(request,'vous avez ete deconnecté')
    return redirect('home')
        

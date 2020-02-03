from django.shortcuts import render, redirect
from django.http import HttpResponse
from foodSystem.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from passlib.hash import pbkdf2_sha256
# from .tokens import account_activation_token

from .models import *
from userSide.models import *

# Create your views here.

def signup(request):
    try:
        if request.method == 'POST':
            admin_username= request.POST['username']
            admin_password= request.POST['password']
            admin_email= request.POST['email']
            # print(admin_username)
            try:
                Admin.objects.get(admin_username = admin_username)
                Admin.objects.get(admin_email = admin_email)
                context = {"msg" : "Already Exists!!"}
                return render(request , "signup.html" , context)
            except:
                Admin.objects.create(
                admin_username=admin_username,
                admin_password=pbkdf2_sha256.hash(admin_password, rounds=1200, salt_size=8), 
                admin_email=admin_email)
                return redirect("/admin/login/")  
        else:
            return render(request,'signup.html')
    except Exception as e:
        print(e)
        print("Caught in Signup")


def menuItem(request):
    try:
        context = {}
        sessionuser = request.session['admin_username']
        if Menuitem.objects.all().exists():
            showMenu = Menuitem.objects.all()
            print("showmenu" , showMenu)
            context = {"object_Show": showMenu}
        else:
            context = {}
        if request.method == 'POST':
            item_name = request.POST['itemName']
            item_price = request.POST['itemPrice']
            try:
                item = Menuitem.objects.get(item_name = item_name.upper())
                print(item)
                context = {"msgExists" : True}
                return render(request, 'menu.html' , context)
            except Exception as e:
                print(e)
                Menuitem.objects.create(
                    item_name = item_name.upper(),
                    item_price = item_price
                )
                if context == {}:
                    context = {"msg" : True}
                else:
                    context = {"object_Show": showMenu , "msg" : True}
                return render(request, 'menu.html' , context)
        else:
            return render(request, 'menu.html' , context)
        return render(request, 'menu.html', context)       
    except Exception as e:
        print("final" , e)
        print("Caught in Menu")
        return redirect("/admin/login/")

def login_session(request):
    try:
        if request.method == 'POST':
            user = request.POST['user']
            passwrd = request.POST['pass']
            try:
                obj = Admin.objects.get(admin_username = user)
                ans = pbkdf2_sha256.verify(passwrd , obj.admin_password)
                if ans == True:
                    request.session['admin_username'] = obj.admin_username
                    return redirect('/admin/home/')
                else:
                    context = {'msg' : 'Incorrect Username or Password!'}
                    return render(request , "login.html" , context)
            except Exception as e:
                print("exception in login",e)
                return redirect("/admin/signup/")
        else:
            return render(request, 'login.html')
    except Exception as e:
        print(e)
        print("Caught in login")


def logout(request):
    try:
        del request.session['admin_username']
        return redirect('/home/')
    except Exception as e:
        print(e)
        print("Caught in logout")


def homePage(request):
    try:
        sessionuser = request.session['admin_username']
        return render(request, "home.html")
    except Exception as e:
        print(e)
        print("Caught in Home Page")
        return redirect('/admin/login/')

def ChngeMenu(request):
    try:
        sessionuser = request.session['admin_username']
        showMenu = Menuitem.objects.all()
        print(showMenu)
        context = {"object_Show": showMenu}
        if request.method == 'GET':
            itemName = request.GET['name']
            newPrice = request.GET['price']
            print(itemName)
            print(newPrice)
            id = request.GET['id']
            print(id)
            obj = Menuitem.objects.get(id = id)
            # print(obj.item_price)
            obj.item_price = newPrice
            obj.item_name = itemName.upper()
            obj.save()
            context = {"object_Show": showMenu , "msg" : True}
            return render(request, 'chngeMenu.html' , context)
        else:
            return render(request , "chngeMenu.html" , context)
        return render(request , "chngeMenu.html" , context)
    except Exception as e:
        print(e)
        print("Caught in Change Menu")
        return redirect("/admin/login/")
    return HttpResponse()

def deleteMenuItem(request):
    try:
        sessionuser = request.session['admin_username']
        showMenu = Menuitem.objects.all()
        context = {"object_Show": showMenu }
        if request.method == 'GET':
            id = request.GET['id']
            obj = Menuitem.objects.get(id = id)
            print(obj)
            obj.delete()
            context = {"object_Show": showMenu , "msg": True}
            return render(request , "deleteItem.html" , context)
        else:
            print("else")
            return render(request , "deleteItem.html" , context)
        return render(request , "deleteItem.html" , context)
    except Exception as e:
        print(e)
        print("Caught in Delete Menu")
        return redirect("/admin/login/")

def viewBill(request):
    try:
        sessionuser = request.session['admin_username']
        if Usermenu.objects.all().exists():
            viewbill = Usermenu.objects.all()
            print("hre" , viewbill)
            for i in viewbill:
                userAdd = Usersignup.objects.get(user_username = i.username)
                context = {"viewbill" : viewbill , "userAdd" : userAdd}
            return render(request , "viewbill.html" , context)
        else:
            context = {"msg" : True}
            return render(request , "home.html" , context)
    except Exception as e:
        print(e)
        print("Caught in View bill")
        return redirect("/admin/login/")

        
def profile(request):
    try:
        session_username = request.session['admin_username']
        obj_profile = Admin.objects.get(admin_username = session_username)
        context = {'objProf' : obj_profile}
        return render(request , "adminprofile.html" , context)
    except Exception as e:
        print(e)
        print("Caught in Profile")
        return redirect("/admin/login/")

def change_password(request):
    try:
        session_username = request.session['admin_username']
        print(session_username)
        if request.method == 'POST':
            oldpswd = request.POST['oldpswd']
            newpswd = request.POST['newpswd']
            try:
                if oldpswd != newpswd:
                    obj = Admin.objects.get(admin_username = session_username)
                    print(obj.admin_password)
                    ans = pbkdf2_sha256.verify(oldpswd , obj.admin_password )
                    if ans == True:
                        obj.admin_password = pbkdf2_sha256.hash(newpswd, rounds=1200, salt_size=8)
                        obj.save()
                        context = {"msg" : "Password Changed!"}
                        return render(request , "chngePassword.html" , context)
                    else:
                        print("false")
                        context = {"msg" : "Password Wrong!"}
                        return render(request , "chngePassword.html" , context)
                else:
                    context = {"msgSame" : True}
                    return render(request , "chngePassword.html" , context)
            except Exception as e:
                print(e)
                context = {"msg" : "Incorrect Password"}
                return render(request , "chngePassword.html" , context)
            # return redirect("/admin/profile")
        else:
            return render(request , "chngePassword.html")
    except Exception as e:
        print(e)
        print("Caught in Change Password")
        return redirect("/admin/login/")

def subscribe(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            uname = request.POST['user']
            try:
                email_info = Admin.objects.get(admin_email = email , admin_username = uname)
            except:
                context = {"msg" : "Account not Found!"}
                return render(request, 'forgetPasswrd.html' , context)
            ids = str(email_info.id)
            subject = 'Your Password Reset Link'
            link = 'http://127.0.0.1:8000/admin/forgetpassword/reset/'+ str(ids)+'/'
            message = 'Hope you are enjoying your Django Tutorials ' + link
            print(email)
            send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            return render(request, 'success.html', {'recepient': email})
        return render(request, 'forgetPasswrd.html')
    except Exception as e:
        print(e)
        print("Caught in Subscribe")


def reset(request, id):
    if request.method == 'POST':
        newPass = request.POST['newPass']
        cnfrmPass = request.POST['cnfrmPass']
        print("new pass",newPass)
        if newPass != cnfrmPass:
            context = {"msg" : True , "id" : id}
            return render(request , "resetemail.html", context)
        else:
            resetPass = Admin.objects.get(id = id)
            resetPass.admin_password = pbkdf2_sha256.hash(newPass, rounds=1200, salt_size=8)
            return redirect("/admin/login/")
    return render(request , "resetemail.html")
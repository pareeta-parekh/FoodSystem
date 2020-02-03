from django.shortcuts import render,redirect
from foodSystem.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from passlib.hash import pbkdf2_sha256
from adminSide.models import *

from .models import *

# Create your views here.

def login(request):
    try:
        if request.method == 'POST':
            user = request.POST['user']
            passwrd = request.POST['pass']
            try:
                obj = Usersignup.objects.get(user_username = user)
                ans = pbkdf2_sha256.verify(passwrd , obj.user_password)
                print(ans)
                if ans == True:
                    request.session['user_username'] = obj.user_username
                    return redirect('/user/home/')
                else:
                    context = {'msg' : 'Incorrect Username or Password!'}
                    return render(request , "userlogin.html" , context)
            except Exception as e:
                print(e)
                return redirect("/user/signup/")
        else:
            return render(request, 'userlogin.html')
    except Exception as e:
        print(e)
        print("Caught in Login")

def userHome(request):
    try:
        sessionuser = request.session['user_username']
        return render(request , "userHome.html")
    except Exception as e:
        print(e)
        print("Caught in User Home Page")

def ShowMenu(request):
    print("in show menu")
    try:
        sessionuser = request.session['user_username']
        print(sessionuser)
            # qty = Usermenu.objects.filter()
        objShow = Menuitem.objects.all()
        itemQty = ""
        for i in objShow:
            print("object show id :",i.id, type(i.id))
            try:
                print("in try")
                qtyshow = Usermenu.objects.get(item_name = i.item_name) 
                itemQty = qtyshow.item_Quanty
                print("qty" , itemQty)
                context = {"object_Show" : objShow , "itemQty" : itemQty}
            except:
                # itemQty = ""
                pass
        print("qty out" , itemQty)   
        context = {"object_Show" : objShow , "itemQty" : itemQty}
        return render(request , "showMenu.html" , context)
    except Exception as e:
        print(e)
        print("Caught in User Show Menu")


def selectMenu(request, id):
    print("in selectMenu")
    try:
        print("in selectMenu")
        sessionuser = request.session['user_username']
        if request.method == 'POST':
            print("in if")
            print(id)
            quanty = request.POST['quantity']
            try:
                print("in try")
                itemObj = Menuitem.objects.get(id = id)
                obj = Usermenu.objects.get(item_name = itemObj.item_name , username = sessionuser)

                print("before" , obj.item_Quanty)

                obj.item_Quanty = int(quanty)

                print("after" , obj.item_Quanty)
                obj.save()
                
                total = int(itemObj.item_price) * int(obj.item_Quanty)
                obj.total = total
                obj.save()
            except:
                print("in except")
                itemObj = Menuitem.objects.get(id = id)
                total = int(itemObj.item_price) * int(quanty)
                Usermenu.objects.create(
                    username = sessionuser,
                    item_name = itemObj.item_name,
                    item_price = itemObj.item_price,
                    item_Quanty = quanty,
                    total = total
                )
            return redirect("/user/displayMenu/")
        else:
            print("else selectMenu")
    except Exception as e:
        print(e)
        print("Caught in User Select Menu")

def order(request):
    try:
        sessionuser = request.session['user_username']
        userorder = Usermenu.objects.filter(username = sessionuser)
        useraddress = Usersignup.objects.get(user_username = sessionuser)
        # showorder = Order.objects.get(username = sessionuser)
        itemTotal = 0
        for i in userorder:
            itemTotal = itemTotal + int(i.total)
            print(itemTotal)
            print(i.item_name)
        
        context = {"userorder" : userorder , "useraddress": useraddress , "itemTotal": itemTotal}
        return render(request , "order.html" , context)
        # return render(request , "order.html")
    except Exception as e:
        print(e)
        print("Caught in User Order Page")

def addtocart(request):
    print("add to cart")
    try:
        sessionuser = request.session['user_username']
        print(sessionuser)
        usercart = Usermenu.objects.filter(username = sessionuser)
        print(usercart)
        itemTotal = 0

        for i in usercart:
            itemTotal = itemTotal + int(i.total)
            print(itemTotal)

        context = {"userCart" : usercart , "itemTotal" : itemTotal}
        return render(request , "addtocart.html" , context)
    except Exception as e:
        print(e)
        print("Caught in User Add to Cart")

def deladdtocart(request):
    print("in delete")
    try:
        sessionuser = request.session['user_username']
        showMenu = Usermenu.objects.filter(username = sessionuser)
        context = {"object_Show": showMenu }
        if request.method == 'GET':
            id = request.GET['id']
            obj = Usermenu.objects.get(id = id)
            print(obj)
            obj.delete()
            context = {"object_Show": showMenu , "msg": True}
            return render(request , "addtocart.html" , context)
        else:
            print("else")
            return render(request , "addtocart.html" , context)
        return render(request , "addtocart.html" , context)
    except Exception as e:
        print(e)
        print("Caught in Delete Add to cart")
        return redirect("/user/login/")



def usersignup(request):
    try:
        if request.method == 'POST':
            user_username = request.POST['username']
            user_password = request.POST['password']
            user_email = request.POST['email']
            user_address = request.POST['address']
            try:
                Usersignup.objects.get(user_username = user_username)
                Usersignup.objects.get(user_email = user_email)
                context = {"msg" : "Already Exists!!"}
                return render(request , "usersignup.html" , context)
            except:
                Usersignup.objects.create(
                user_username=user_username,
                user_password=pbkdf2_sha256.hash(user_password, rounds=1200, salt_size=8),
                user_email=user_email,
                user_address=user_address 
                )
                return redirect('/user/login/')  
        else:
            return render(request,'userSignup.html')
    except Exception as e:
        print(e)
        print("Caught in User Signup Page")

def profile(request):
    try:
        session_username = request.session['user_username']
        obj_profile = Usersignup.objects.get(user_username = session_username)
        context = {'objProf' : obj_profile}
        return render(request , "userprofile.html" , context)
    except Exception as e:
        print(e)
        print("Caught in User Profile Page")
    

def changePassword(request):
    print("chnge password")
    try:
        session_username = request.session['user_username']
        if request.method == 'POST':
            oldpswd = request.POST['oldpswd']
            newpswd = request.POST['newpswd']
            try:
                if oldpswd != newpswd:
                    print("in if")
                    obj = Usersignup.objects.get(user_username = session_username)
                    ans = pbkdf2_sha256.verify(oldpswd , obj.user_password)
                    print(ans)
                    if ans == True:
                        obj.user_password = pbkdf2_sha256.hash(newpswd, rounds=1200, salt_size=8)
                        obj.save()
                        context = {"msg" : "Password Changed!!"}
                        return render(request , "userChangePassword.html" , context)
                    else:
                        context = {"msg" : "Password Incorrect!"}
                        return render(request , "userChangePassword.html" , context)
                else:
                    context = {"msgSame" : True}
                    return render(request , "userChangePassword.html" , context)
            except Exception as e:
                print(e)
                context = {"msg" : True}
                return render(request , "userChangePassword.html" , context)
            # return redirect("/user/profile")
        else:
            return render(request , "userChangePassword.html")
    except Exception as e:
        print(e)
        print("Caught in User Change Password Page")

def changeAddress(request):
    try:
        session_username = request.session['user_username']
        if request.method == 'POST':
            newAdd = request.POST['newAdd']

            obj = Usersignup.objects.get(user_username = session_username)
            # print(obj.item_price)
            obj.user_address = newAdd
            obj.save()
            return redirect("/user/profile/")
        else:
            return render(request , "userChangeAddress.html")
    except Exception as e:
        print(e)
        print("Caught in User Change Address Page")

def logout(request):
    try:
        sessionuser = request.session['user_username']
        # userobj = Usermenu.objects.filter(username = sessionuser)
        # userobj.delete()
        del request.session['user_username']
        return render(request , "userlogout.html")
    except Exception as e:
        print(e)
        print("Caught in User Logout Page")

def subscribe(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            uname = request.POST['user']
            try:
                email_info = Usersignup.objects.get(user_email = email , user_username = uname)
            except:
                context = {"msg" : "Account Not Found!"}
                return render(request, 'forgetPasswrd.html' , context)
            ids = str(email_info.id)
            subject = 'Your Password Reset Link'
            # button = '<html> <body> <button> HI </button></body> </html>'
            link = 'http://127.0.0.1:8000/user/forgetpassword/reset/'+ str(ids)+'/'
            message =  link 
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
        print("new pass",newPass)
        resetPass = Usersignup.objects.get(id = id)
        resetPass.user_password = newPass
        return redirect("/user/login/")
    return render(request , "resetemail.html")
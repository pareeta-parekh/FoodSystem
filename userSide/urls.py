from django.urls import path

from .views import *

urlpatterns = [
    path('home/' ,userHome),
    path('displayMenu/' ,ShowMenu),
    path('login/', login),
    path('signup/' ,usersignup),
    path('profile/' ,profile),
    path('profile/changePassword/' ,changePassword),
    path('profile/changeAddress/' ,changeAddress),
    path('selectMenu/<int:id>/', selectMenu, name="selectMenu/"),
    path('displayMenu/cart/' ,addtocart),
    path('displayMenu/cart/order/' ,order),
    path('displayMenu/cart/order/logout/' ,logout),
    path('forgetpassword/' ,subscribe),
    path('forgetpassword/reset/<str:id>/' , reset),
    path('displayMenu/cart/delete/' ,deladdtocart),
]
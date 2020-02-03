from django.urls import path

from .views import(
    signup,
    menuItem,
    login_session,
    homePage,
    logout,
    ChngeMenu,
    viewBill,
    deleteMenuItem,
    profile,
    change_password,
    subscribe,
    reset
)

urlpatterns = [
    path('home/',homePage),
    path('signup/',signup),
    path('menu/' ,menuItem),
    path('menu/change/', ChngeMenu),
    path('menu/delete/', deleteMenuItem),
    path('viewbill/' , viewBill),
    path('login/' ,login_session),
    path('logout/' ,logout),
    path('forgetpassword/' ,subscribe),
    path('forgetpassword/reset/<str:id>/' , reset),
    path('profile/' ,profile),
    path('profile/change_password/',change_password),
]
from django.db import models

# Create your models here.

class Usermenu(models.Model):

    username = models.CharField( max_length = 20)
    item_name = models.CharField(max_length = 20)
    item_price = models.CharField(max_length = 20)
    item_Quanty = models.IntegerField()
    total = models.IntegerField()


class Usersignup(models.Model):
    user_username = models.CharField(max_length = 20 )
    user_password = models.CharField(max_length = 20 )
    user_email = models.CharField(max_length = 30 )
    user_address = models.CharField(max_length = 100)

class Order(models.Model):
    username = models.CharField(max_length = 20)
    useraddress = models.CharField(max_length = 100)
    totalprice = models.IntegerField()

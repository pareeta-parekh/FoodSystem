from django.db import models

# Create your models here.

class Admin(models.Model):
    
    # admin_id = models.IntegerField(unique = True )
    admin_username = models.CharField(max_length = 20 )
    admin_password = models.CharField(max_length = 20 )
    admin_email = models.CharField(max_length = 30 )


class Menuitem(models.Model):

    # item_id = models.CharField(unique = True, max_length = 4 , null = False)
    item_name = models.CharField(max_length = 25 , null = False)
    item_price = models.IntegerField(null = False)
    # item_image = models.FileField()


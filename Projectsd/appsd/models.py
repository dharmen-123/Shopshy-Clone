from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage
import pkg_resources
# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    number=models.IntegerField()
    password=models.CharField()

    class Meta():
       db_table='User'
       verbose_name_plural='User'

class Query(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()    
    userquery=models.TextField()
    class Meta():
        db_table='Query'
        verbose_name_plural='Query'

class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    category=models.CharField(max_length=100)
    mrp=models.IntegerField()
    offprice=models.IntegerField()
    rating=models.FloatField()
    itemtype=models.CharField(max_length=100)
    color=models.CharField(max_length=60)
    
    class Meta():
        db_table='Products'
        verbose_name_plural='Product'
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_data')
    images=models.ImageField(upload_to='images/',storage=MediaCloudinaryStorage())
    
    class Meta():
        db_table='ProductImages'
        verbose_name_plural='ProductImages'
    def __str__(self):
        return self.product.name

class Payment(models.Model):
    user_id=models.IntegerField()
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField()  
    status = models.CharField(max_length=20, default="Created")  
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        db_table='Payment' 

class Address(models.Model):
    userid=models.CharField(max_length=100)
    alternateno=models.IntegerField()   
    address1=models.CharField(max_length=250)
    address2=models.CharField(max_length=250)
    country=models.CharField(max_length=100)
    zipcode=models.IntegerField()
    city=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    
    class Meta():
        db_table='Address'
        verbose_name_plural='Address'
        
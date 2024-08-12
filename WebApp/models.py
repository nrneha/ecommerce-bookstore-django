from django.db import models

# Create your models here.

class CustomerDB(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Subject = models.EmailField(max_length=100,null=True,blank=True)
    Message = models.TextField(null=True,blank=True)

class User_Accounts(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Password = models.CharField(max_length=100,null=True,blank=True)

class CartDB(models.Model):
    Customer = models.CharField(max_length=100,null=True,blank=True)
    Book = models.CharField(max_length=100,null=True,blank=True)
    Price = models.IntegerField(null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Total = models.IntegerField(null=True,blank=True)

class CheckOutDB(models.Model):
    Customer = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(max_length=100, null=True, blank=True)
    Mobile = models.TextField(max_length=100, null=True, blank=True)
    Address = models.TextField(max_length=100, null=True, blank=True)
    Total = models.IntegerField(null=True,blank=True)

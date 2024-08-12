from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class CategoryDB(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Image = models.ImageField(upload_to="Category Image", null=True, blank=True)


class BooksDB(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Category = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Price = models.IntegerField(null=True, blank=True)
    Image = models.ImageField(upload_to="Books Image", null=True, blank=True)

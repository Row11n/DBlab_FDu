from django.db import models

# Create your models here.

class Book(models.Model):
    ISBN = models.CharField(max_length = 13, primary_key=True)
    name = models.CharField(max_length = 50)
    publisher = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
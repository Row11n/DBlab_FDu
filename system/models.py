from django.db import models

# Create your models here.

class Book(models.Model):
    IBSN = models.CharField(max_length = 13, primary_key=True)
    name = models.CharField(max_length = 50)
    publisher = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name
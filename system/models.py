from django.db import models
from Userinfo.models import *

# Create your models here.

class Book_info(models.Model):
    ISBN = models.CharField(max_length = 13, unique=True, null=False)
    name = models.CharField(max_length = 50, null=False)
    publisher = models.CharField(max_length = 50, null=False)
    author = models.CharField(max_length = 50, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=0)
    def __str__(self):
        return self.name

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book_info, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    amount = models.PositiveIntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    
    @property
    def totalprice(self):
        return self.price * self.amount

    def __str__(self):
        return self.book.name

class Stock_bill(Bill):
    STATUS_TYPE = (
        ("1","未付款"),
        ("2","已付款"),
        ("3","已退货"),
        ("4","已到货"),
        ("5","已入库"),
    )
    status = models.CharField(max_length=2, choices=STATUS_TYPE, verbose_name="状态", default="1")


    @property
    def getstatus(self):
        return self.get_status_display()

class Guest_bill(Bill):
    STATUS_TYPE = (
        ("1","未付款"),
        ("2","已付款"),
    )
    status = models.CharField(max_length=2, choices=STATUS_TYPE, verbose_name="状态", default="1")
    def getstatus(self):
        return self.get_status_display()


class Finance(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_stock = models.BooleanField(default=1)
    
    @property
    def type(self):
        if self.is_stock == 1:
            return "进货"
        else:
            return "买书"
    
    @property
    def user(self):
        return self.bill.user

    @property
    def income(self):
        if self.is_stock == 1:
            return -(self.bill.totalprice)
        else:
            return self.bill.totalprice

    
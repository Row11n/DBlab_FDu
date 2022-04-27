from django.shortcuts import render
from .models import Book

# Create your views here.

def home(request):
    return render(request, 'system/home.html')

def books(request):
    books = Book.objects.order_by('ISBN')
    context = {'books':books}
    return render(request, 'system/books_display.html', context)
from django.shortcuts import render, redirect
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import *


# Create your views here.

def home(request):
    return render(request, 'system/home.html')

@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class BooksView(View):
    def get(self, request):
        srch_ISBN = request.GET.get('search_ISBN')
        srch_name = request.GET.get('search_name')
        srch_publisher = request.GET.get('search_publisher')
        srch_author = request.GET.get('search_author')
        books = Book_info.objects.all()
        if srch_ISBN is None:
            srch_ISBN = ''
        if srch_name is None:
            srch_name = ''
        if srch_publisher is None:
            srch_publisher = ''
        if srch_author is None:
            srch_author = ''
        books_list = list(books.filter(ISBN__icontains=srch_ISBN,name__icontains=srch_name,
                                        publisher__icontains=srch_publisher,author__icontains=srch_author))
        return render(request, 'system/books_display.html',
            context={'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,})

    def post(self, request):
        ...

@method_decorator(login_required(login_url='/Userinfo/login/'), name='dispatch')
class InfoDetailView(View):
    template = 'system/info_detail.html'

    def get(self, request, book_id):
        book_info = Book_info.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info)
        return render(request, self.template, 
            context={'form': form,'book_info':book_info})

    def post(self, request, book_id):
        book_info = Book_info.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info,data=request.POST)
        a = form.data.get('is_active')
        
        if form.is_valid():
            print(form) 
            form.save()
            return render(request, self.template, 
                context={'form': form,'book_info':book_info})
        else:
            return render(request, self.template,
                context={'form': form,'book_info':book_info,'error_msg': '检查输入格式！'})


class StockBillsView(View):
    def get(self, request):
        form = StockStatusForm()
        bills_list = list(Stock_bill.objects.all())
        return render(request, 'system/stockbills.html', 
            context={'form':form,'bills_list':bills_list})

    def post(self, request):
        form = StockStatusForm(data=request.POST)
        bill_id = form.data.get('bill_id')
        pay= form.data.get('pay')
        send_back = form.data.get('send_back')
        arrival = form.data.get('arrival')
        bill = Stock_bill.objects.get(id = bill_id)
        bills_list = list(Stock_bill.objects.all())
        print(bill.status)
        print(pay)
        if bill.status == "1" and pay == "1":
            print(pay)
            bill.status = "2"
            bill.save()
            finan = Finance(bill=bill, is_stock=1)
            finan.save()
        
        elif bill.status == "1" and send_back == "1":
            bill.status = "3"
            bill.save()

        elif bill.status == "2" and arrival == "1":
            bill.status = "4"
            bill.save()

        elif  bill.status == "4":
            book = Book_info.objects.get(id = bill.book.id)
            print(123)
            bill.status = "5"
            book.amount = book.amount + bill.amount
            book.save()
            bill.save()
            

        return redirect('system:stockbills')


class StockView(View):  
    def get(self, request):
        srch_ISBN = request.GET.get('search_ISBN')
        books = Book_info.objects.all()
        if srch_ISBN is None or srch_ISBN == '':
            form = StockForm()
            books_list = [1,2]
            return render(request, 'system/stock.html', 
                    context={'form':form, 'books_list':books_list})
        books_list = books.filter(ISBN__icontains=srch_ISBN)
        book = books_list.first()
        form = StockForm(initial={'book': book})
        return render(request, 'system/stock.html', 
            context={'form':form, 'books_list':books_list})

    def post(self, request):
        form = StockForm(data=request.POST)
        user_id = form.data.get('user_id')
        if form.is_valid():
            book_id = form.data.get('book')
            price = form.data.get('price')
            amount = form.data.get('amount')
            print(user_id)
            user = User.objects.get(id = user_id)
            book = Book_info.objects.get(id = book_id)
            stockbill = Stock_bill(book=book,price=price,amount=amount,user=user)
            stockbill.save()
            return redirect('system:stockbills')
        else:
            return render(request, 'system/stock.html', 
                context={'form':form, 'error_msg':'检查输入格式'})


class NewBookView(View):
    def get(self, request):
        form = BookInfoForm()
        return render(request, 'system/new_book.html', 
            context={'form':form})

    def post(self, request):
        form = BookInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('system:books')
        else:
            return render(request, 'system/new_book.html', 
                context={'form':form, 'error_msg':'检查输入格式'})

class FinanceView(View):
    def get(self, request):
        finance_list = Finance.objects.all()
        return render(request, 'system/finance.html', 
            context={'finance_list':finance_list})

    def post(self, request):
        ...


class BookShopView(View):
    def get(self, request):
        books_list = Book_info.objects.filter(amount__gt=0, price__gt=0, is_active=1)
        return render(request, 'system/bookshop.html', 
            context={'books_list':books_list})

    def post(self, request):
        ...
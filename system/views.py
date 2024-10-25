from django.shortcuts import render, redirect
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import *
from django.http import Http404
import datetime

# Create your views here.

def home(request):
    return render(request, 'system/home.html')  

def about(request):
    return render(request, 'system/about.html')  

def ranking(request):
    orders_with_total_quantity = Bill.objects.values('book_id').annotate(total_quantity=Sum('amount'))
    print(orders_with_total_quantity)
    return render(request, 'system/ranking.html', {'dynamics': orders_with_total_quantity})


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class BooksView(View):
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
        form = BookInfoForm()
        srch_ISBN = request.GET.get('search_ISBN')
        srch_name = request.GET.get('search_name')
        srch_publisher = request.GET.get('search_publisher')
        srch_author = request.GET.get('search_author')
        books = Book_info.objects.all() #获取所有图书
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
            context={'form':form,'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,})

    def post(self, request):
        form = BookInfoForm(data=request.POST)
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
        activate = form.data.get('activate')
        deactivate= form.data.get('deactivate')
        ISBN= form.data.get('ISBN')
        book = Book_info.objects.get(ISBN=ISBN)
        if(form.data.get('price')):
            price = form.data.get('price')
            if(float(price) <= 0):
                return render(request, 'system/books_display.html',
            context={'form':form,'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,
                        'error_msg':'售价必须大于0！','wrong_ISBN':ISBN})
        if(activate):
            if(book.amount == 0):
                return render(request, 'system/books_display.html',
            context={'form':form,'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,
                        'error_msg':'库存不够，请先进货！','wrong_ISBN':ISBN})
            book.price = price
            book.is_active = 1
            book.save()
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
            context={'form':form,'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,})
        
        if(deactivate):
            book.is_active = 0
            book.save()
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
            context={'form':form,'books_list': books_list,'ISBN':srch_ISBN,'name':srch_name,'author':srch_author,'publisher':srch_publisher,})



@method_decorator(login_required(login_url='/Userinfo/login/'), name='dispatch')
class InfoDetailView(View):
    template = 'system/info_detail.html'

    def get(self, request, book_id):
        if(request.user.is_staff == False):
            raise Http404
        book_info = Book_info.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info)
        return render(request, self.template, 
            context={'form': form,'book_info':book_info})

    def post(self, request, book_id):
        book_info = Book_info.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info,data=request.POST) 
        if form.is_valid():
            print(form) 
            form.save()
            return render(request, self.template, 
                context={'form': form,'book_info':book_info})
        else:
            print(form.errors)
            return render(request, self.template,
                context={'form': form,'book_info':book_info,'error_msg': '检查输入格式！'})


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class StockBillsView(View):
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
        form = StockStatusForm()
        bills_list = list(Stock_bill.objects.all().order_by('status'))
        return render(request, 'system/stockbills.html', 
            context={'form':form,'bills_list':bills_list})

    def post(self, request):
        form = StockStatusForm(data=request.POST)
        bill_id = form.data.get('bill_id')
        pay= form.data.get('pay')
        send_back = form.data.get('send_back')
        arrival = form.data.get('arrival')
        bill = Stock_bill.objects.get(id = bill_id)
        bills_list = list(Stock_bill.objects.all().order_by('status'))
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

@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class StockView(View):  
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
        srch_ISBN = request.GET.get('search_ISBN')
        books = Book_info.objects.all()
        if srch_ISBN is None or srch_ISBN == '':
            form = StockForm()
            books_list = [1,2]
            return render(request, 'system/stock.html', 
                    context={'form':form, 'books_list':books_list})
        books_list = books.filter(ISBN=srch_ISBN)
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

@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class NewBookView(View):
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
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

@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class NewBookForStockView(View):
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
        form = BookInfoForm()
        return render(request, 'system/new_book_for_stock.html', 
            context={'form':form})

    def post(self, request):
        form = BookInfoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('system:stock')
        else:
            return render(request, 'system/new_book_for_stock.html', 
                context={'form':form, 'error_msg':'检查输入格式'})


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class FinanceView(View):
    def get(self, request):
        if(request.user.is_staff == False):
            raise Http404
        start = request.GET.get('search_start')
        end = request.GET.get('search_end')
        if start is None or start == '':
            start = '2022-05-01'
        if end is None or end == '':
            end = '2022-12-31'
        print(end)
        end = end + ' 23:59:59'
        finance_list = list(Finance.objects.filter(date__gte=start,date__lte=end).order_by('-date'))
        profit = 0
        out_ = 0
        in_ = 0
        for finance in finance_list:
            profit = profit + finance.income_int
            if(finance.income_int > 0):
                in_ = in_ + finance.income_int
            if(finance.income_int < 0):
                out_ = out_ + finance.income_int
        print(profit)
        return render(request, 'system/finance.html', 
            context={'finance_list':finance_list,'start':start, 'end':end, 'profit':profit,'in_':in_, 'out_':out_})

    def post(self, request):
        ...

@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class BookShopView(View):
    def get(self, request):
        books_list = Book_info.objects.filter(is_active=1)
        form = GuestForm()
        return render(request, 'system/bookshop.html', 
            context={'form':form,'books_list':books_list})

    def post(self, request):
        books_list = Book_info.objects.filter(amount__gt=0, price__gt=0, is_active=1)
        form = GuestForm(data=request.POST)
        amount = form.data.get('amount')
        book_ISBN = form.data.get('book_ISBN')
        price = form.data.get('price')
        user_id = form.data.get('user_id')
        book = Book_info.objects.get(ISBN=book_ISBN)
        if(amount is None or amount == ''):
            return render(request, 'system/bookshop.html', 
            context={'form':form,'books_list':books_list,'error_msg':'请输入购买量！','wrong_ISBN':book_ISBN})
        if book.amount - int(amount) < 0:
            return render(request, 'system/bookshop.html', 
            context={'form':form,'books_list':books_list,'error_msg':'库存不足，请重新选择购买量','wrong_ISBN':book_ISBN})
        book.amount = book.amount - int(amount)
        book.save()
        user = User.objects.get(id=user_id)
        guestbill = Guest_bill(book=book, user = user, price = price, amount = amount)
        guestbill.save()
        return redirect('system:bookshop')

        
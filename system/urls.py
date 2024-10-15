from django.urls import path
from . import views

app_name = 'system'

urlpatterns = [
    path('', views.home, name='home'),
    path('books', views.BooksView.as_view(), name='books'),
    path('info_detail/<int:book_id>/', views.InfoDetailView.as_view(), name='info_detail'),
    path('stockbills', views.StockBillsView.as_view(), name='stockbills'),
    path('stock', views.StockView.as_view(), name='stock'),
    path('new_book', views.NewBookView.as_view(), name='new_book'),
    path('new_book_for_stock', views.NewBookForStockView.as_view(), name='new_book_for_stock'),
    path('finance', views.FinanceView.as_view(), name='finance'),
    path('bookshop', views.BookShopView.as_view(), name='bookshop'),
    path('ranking', views.ranking, name='ranking'),
    
    path('about', views.about, name='about'),
]
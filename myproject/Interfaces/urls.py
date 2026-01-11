from django.urls import path
from . import views

urlpatterns = [
    # Головна точка входу (перенаправлення)
    path('', views.index_dispatch, name='index'),



    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('admin-stats-plotly/', views.admin_stats_plotly, name='admin_stats_plotly'),
    path('admin-stats-bokeh/', views.admin_stats_bokeh, name='admin_stats_bokeh'),
    path('admin-stats-concurrency/', views.admin_stats_concurrency, name='admin_stats_concurrency'),


    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('balance/add/', views.add_balance, name='add_balance'),
    path('book/return/', views.return_book_view, name='return_book_view'),


    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_form, name='book_create'),
    path('book/<int:pk>/edit/', views.book_form, name='book_update'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),

    path('book/<int:pk>/buy/', views.buy_book, name='buy_book'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
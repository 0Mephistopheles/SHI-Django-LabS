from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from DB_Management.repositories.unit_of_work import UnitOfWork
from .forms import BookForm
from DB_Management.models import UserProfile, Customer, Bookorder, Bookorderitem
from django.utils import timezone

from DB_Management.services.plotly_service import PlotlyVisualizationService
from django.core.cache import cache
from django.shortcuts import render
from DB_Management.repositories.unit_of_work import UnitOfWork
from DB_Management.services.seaborn_service import SeabornVisualizationService
from DB_Management.services.concurrency_service import ConcurrencyService
import pandas as pd


@login_required
def admin_stats_plotly(request):
    if not request.user.is_superuser:
        return redirect('index')

    # Отримання параметрів фільтрації
    threshold = int(request.GET.get('threshold', 100))
    author_query = request.GET.get('author_query', '').strip()
    min_books = int(request.GET.get('min_books', 1))
    min_spent = float(request.GET.get('min_spent', 0))
    top_genres = request.GET.get('top_genres', 10)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Динамічний ключ кешу
    cache_key = f"plotly_{threshold}_{author_query}_{min_books}_{min_spent}_{top_genres}_{start_date}_{end_date}"
    charts = cache.get(cache_key)

    if not charts:
        uow = UnitOfWork()
        viz = PlotlyVisualizationService()
        charts = {}

        df_authors = pd.DataFrame(list(uow.analytics.get_books_count_by_author(author_query, min_books)))
        df_genres = pd.DataFrame(list(uow.analytics.get_popularity_by_genre(top_genres)))
        df_sales = pd.DataFrame(list(uow.analytics.get_monthly_sales_dynamics(start_date, end_date)))
        df_customers = pd.DataFrame(list(uow.analytics.get_total_spent_by_customer(min_spent)))
        df_publishers = pd.DataFrame(list(uow.analytics.get_publisher_book_stats()))
        df_stock = pd.DataFrame(list(uow.analytics.get_low_stock_warehouses(threshold)))

        charts['author_chart'] = viz.generate_author_bar(df_authors)
        charts['genre_chart'] = viz.generate_genre_pie(df_genres)
        charts['sales_chart'] = viz.generate_sales_line(df_sales)
        charts['customer_chart'] = viz.generate_customer_bar(df_customers)
        charts['publisher_chart'] = viz.generate_publisher_bar(df_publishers)
        charts['stock_chart'] = viz.generate_stock_bar(df_stock)

        cache.set(cache_key, charts, 300)

    context = {
        'charts': charts,
        'filters': {
            'threshold': threshold, 'author_query': author_query,
            'min_books': min_books, 'min_spent': min_spent,
            'top_genres': top_genres, 'start_date': start_date, 'end_date': end_date
        }
    }
    return render(request, 'Interfaces/admin_stats_plotly.html', context)

@login_required
def admin_stats(request):
    charts = cache.get('admin_analytics_charts_v2') # Окремий ключ для кешу

    if not charts:
        uow = UnitOfWork()
        viz = SeabornVisualizationService()
        conc_service = ConcurrencyService()
        charts = {}

        df_authors = pd.DataFrame(list(uow.analytics.get_books_count_by_author()))
        if not df_authors.empty:
            df_authors['full_name'] = df_authors['firstname'] + ' ' + df_authors['lastname']
            charts['author_chart'] = viz.generate_bar(df_authors, 'books_count', 'full_name')

        df_genres = pd.DataFrame(list(uow.analytics.get_popularity_by_genre()))
        charts['genre_chart'] = viz.generate_pie(df_genres, 'total_sold', 'genre')

        df_sales = pd.DataFrame(list(uow.analytics.get_monthly_sales_dynamics()))
        if not df_sales.empty:
            df_sales['month_str'] = df_sales['month'].dt.strftime('%b %Y')
            charts['sales_chart'] = viz.generate_line(df_sales, 'month_str', 'total_revenue')

        df_customers = pd.DataFrame(list(uow.analytics.get_total_spent_by_customer()))
        if not df_customers.empty:
            df_customers['name'] = df_customers['customerid__firstname'] + ' ' + df_customers['customerid__lastname']
            charts['customer_chart'] = viz.generate_bar(df_customers, 'total_spent', 'name',
                                                        color="magma")

        df_publishers = pd.DataFrame(list(uow.analytics.get_publisher_book_stats()))
        charts['publisher_chart'] = viz.generate_bar(df_publishers, 'books_published', 'name',
                                                     color="coolwarm")

        df_stock = pd.DataFrame(list(uow.analytics.get_low_stock_warehouses()))
        charts['stock_chart'] = viz.generate_bar(df_stock, 'total_books', 'location',
                                                 color="Reds_r")

        cache.set('admin_analytics_charts', charts, 10)


        performance_data = conc_service.run_experiment(total_requests=150)
        df_perf = pd.DataFrame(performance_data)
        
        # Генерація графіка продуктивності
        charts['performance_chart'] = viz.generate_performance_chart(df_perf)

        cache.set('admin_analytics_charts_v2', charts, 60) # Кешуємо на 1 хвилину

    return render(request, 'Interfaces/admin_stats.html', {'charts': charts})


@login_required
def index_dispatch(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')  # Захист від звичайних юзерів

    return render(request, 'Interfaces/admin_dashboard.html')




@login_required
def user_dashboard(request):
    # Отримуємо профіль для відображення балансу
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Fallback якщо профіль не створився автоматично
        profile = UserProfile.objects.create(user=request.user)

    return render(request, 'Interfaces/user_dashboard.html', {'balance': profile.balance})


@login_required
def add_balance(request):
    """
    Гіперпосилання 'додати 100 грн'
    """
    profile = request.user.userprofile
    profile.balance += 100
    profile.save()
    return redirect('user_dashboard')


@login_required
def return_book_view(request):
    """
    Віддати свою книгу: додаємо книгу в базу + нараховуємо 200 грн.
    """
    uow = UnitOfWork()  #

    if request.method == 'POST':
        form = BookForm(request.POST)  #
        if form.is_valid():
            data = form.cleaned_data

            # 1. Додаємо книгу через репозиторій
            uow.books.create(data)

            # 2. Нараховуємо баланс користувачу
            profile = request.user.userprofile
            profile.balance += 200
            profile.save()

            return redirect('user_dashboard')
    else:
        form = BookForm()

    return render(request, 'Interfaces/return_book.html', {'form': form})




def book_list(request):
    uow = UnitOfWork()
    books = uow.books.get_all()  #
    return render(request, 'Interfaces/book_list.html', {'books': books, 'is_admin': request.user.is_superuser})


@login_required
def book_detail(request, pk):
    uow = UnitOfWork()
    book = uow.books.get_by_id(pk)

    if not book:
        raise Http404("Книгу не знайдено")

    return render(request, 'Interfaces/book_detail.html', {
        'book': book,
        'is_admin': request.user.is_superuser
    })

@login_required
def book_form(request, pk=None):
    if pk and not request.user.is_superuser:
        return HttpResponseForbidden("Тільки адміністратор може редагувати книги.")

    uow = UnitOfWork()
    book = None
    title = "Додавання нової книги"

    if pk:
        book = uow.books.get_by_id(pk)
        if not book:
            raise Http404("Книгу не знайдено")
        title = "Редагування книги"

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            data = form.cleaned_data
            if pk:
                uow.books.update(pk, data)
            else:
                uow.books.create(data)

            if request.user.is_superuser:
                return redirect('book_list')
            else:
                return redirect('user_dashboard')
    else:
        form = BookForm(instance=book)

    return render(request, 'Interfaces/book_form.html', {'form': form, 'title': title})


@login_required
def book_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Тільки адміністратор може видаляти книги.")

    uow = UnitOfWork()
    book = uow.books.get_by_id(pk)
    if not book:
        raise Http404("Книгу не знайдено")

    if request.method == 'POST':
        uow.books.delete_by_id(pk)
        return redirect('book_list')

    return render(request, 'Interfaces/book_confirm_delete.html', {'book': book})


@login_required
def buy_book(request, pk):
    uow = UnitOfWork()
    book = uow.books.get_by_id(pk)
    if not book:
        raise Http404("Книгу не знайдено")

    price = 150.00

    profile = request.user.userprofile

    if profile.balance < price:
        return render(request, 'Interfaces/order_error.html', {'message': 'Недостатньо коштів на балансі!'})

    customer = Customer.objects.filter(email=request.user.email).first()
    if not customer:
        customer = Customer.objects.create(
            firstname=request.user.first_name or request.user.username,
            lastname=request.user.last_name or "User",
            email=request.user.email or f"{request.user.username}@example.com",
            phonenumber="",
            address=""
        )


    with uow:
        order_data = {
            'customerid': customer,
            'orderdate': timezone.now(),
            'totalamount': price,
            'paymentstatus': 'Paid'
        }
        order = uow.orders.create(order_data)

        Bookorderitem.objects.create(
            orderid=order,
            bookid=book,
            quantity=1,
            unitprice=price
        )

        profile.balance = float(profile.balance) - price
        profile.save()

    return redirect('my_orders')


@login_required
def my_orders(request):
    uow = UnitOfWork()
    email = request.user.email or f"{request.user.username}@example.com"
    orders = uow.orders.get_by_email(email)


    return render(request, 'Interfaces/my_orders.html', {'orders': orders})


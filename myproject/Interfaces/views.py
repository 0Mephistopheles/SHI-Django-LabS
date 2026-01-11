from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from DB_Management.repositories.unit_of_work import UnitOfWork
from .forms import BookForm
from DB_Management.models import UserProfile, Customer, Bookorder, Bookorderitem
from django.utils import timezone

from DB_Management.services.concurrency_service import ConcurrencyService
from DB_Management.services.plotly_service import PlotlyVisualizationService
from django.core.cache import cache
from django.shortcuts import render
from DB_Management.repositories.unit_of_work import UnitOfWork
from DB_Management.services.dataframe_service import AnalyticsDataFrameService
from DB_Management.services.plotly_service import PlotlyVisualizationService
from DB_Management.services.seaborn_service import SeabornVisualizationService
from DB_Management.services.bokeh_service import BokehVisualizationService


def get_analytics_filters(request):
    """
    Отримує параметри безпечно. Не скидає все, якщо один параметр битий.
    """
    filters = {}

    # Helper для безпечного int
    def get_int(key, default):
        try:
            val = request.GET.get(key)
            return int(val) if val is not None and val != '' else default
        except (ValueError, TypeError):
            return default

    # Helper для безпечного float
    def get_float(key, default):
        try:
            val = request.GET.get(key)
            return float(val) if val is not None and val != '' else default
        except (ValueError, TypeError):
            return default

    filters['threshold'] = get_int('threshold', 100)
    filters['min_books'] = get_int('min_books', 0)
    filters['min_spent'] = get_float('min_spent', 0.0)

    # Top Genres може бути None
    top_genres = request.GET.get('top_genres')
    if top_genres and top_genres.isdigit():
        filters['top_genres'] = int(top_genres)
    else:
        filters['top_genres'] = None  # None означає "всі"

    filters['author_query'] = request.GET.get('author_query', '').strip()

    # Дати залишаємо рядками, сервіс/ORM розбереться
    filters['start_date'] = request.GET.get('start_date') or None
    filters['end_date'] = request.GET.get('end_date') or None

    # DEBUG: Виводимо в консоль, щоб ви бачили, що приходить
    print(f"DEBUG FILTERS: {filters}")

    return filters

@login_required
def admin_stats_bokeh(request):
    if not request.user.is_superuser: return redirect('index')

    filters = get_analytics_filters(request)
    cache_key = f"bokeh_unified_v12_{filters}"
    cached_payload = cache.get(cache_key)

    if not cached_payload:
        # 1. Отримуємо дані
        data_service = AnalyticsDataFrameService()
        dfs = data_service.get_filtered_data(filters)
        stats = data_service.get_stats_kpi(dfs)

        # 2. Малюємо (Bokeh)
        viz = BokehVisualizationService()
        charts = {
            'author_chart': viz.generate_author_bar(dfs['authors']),
            'genre_chart': viz.generate_genre_pie(dfs['genres']),
            'sales_chart': viz.generate_sales_line(dfs['sales']),
            'customer_chart': viz.generate_customer_bar(dfs['customers']),
            'publisher_chart': viz.generate_publisher_bar(dfs['publishers']),
            'stock_chart': viz.generate_stock_bar(dfs['stock']),
        }
        cached_payload = {'charts': charts, 'stats': stats}
        cache.set(cache_key, cached_payload, 30)

    return render(request, 'Interfaces/admin_stats_bokeh.html', {
        'charts': cached_payload['charts'],
        'stats': cached_payload['stats'],
        'filters': filters
    })

def admin_stats_plotly(request):
    if not request.user.is_superuser: return redirect('index')

    filters = get_analytics_filters(request)
    # Змінюємо ключ кешу, щоб скинути старе
    cache_key = f"plotly_unified_v12_{filters}"
    cached_payload = cache.get(cache_key)

    if not cached_payload:
        # 1. Отримуємо дані (Єдине джерело правди)
        data_service = AnalyticsDataFrameService()
        dfs = data_service.get_filtered_data(filters)
        stats = data_service.get_stats_kpi(dfs)

        # 2. Малюємо (Plotly)
        viz = PlotlyVisualizationService()
        charts = {
            'author_chart': viz.generate_author_bar(dfs['authors']),
            'genre_chart': viz.generate_genre_pie(dfs['genres']),
            'sales_chart': viz.generate_sales_line(dfs['sales']),
            'customer_chart': viz.generate_customer_bar(dfs['customers']),
            'publisher_chart': viz.generate_publisher_bar(dfs['publishers']),
            'stock_chart': viz.generate_stock_bar(dfs['stock']),

        }
        cached_payload = {'charts': charts, 'stats': stats}
        cache.set(cache_key, cached_payload, 30)

    return render(request, 'Interfaces/admin_stats_plotly.html', {
        'charts': cached_payload['charts'],
        'stats': cached_payload['stats'],
        'filters': filters
    })

@login_required
def admin_stats(request):
    if not request.user.is_superuser: return redirect('index')

    filters = get_analytics_filters(request)
    cache_key = f"seaborn_unified_v12_{filters}"
    cached_payload = cache.get(cache_key)

    if not cached_payload:
        # 1. Отримуємо ТІ Ж САМІ дані
        data_service = AnalyticsDataFrameService()
        dfs = data_service.get_filtered_data(filters)
        stats = data_service.get_stats_kpi(dfs)

        # 2. Малюємо (Seaborn)
        viz = SeabornVisualizationService()
        charts = {
            'author_chart': viz.generate_author_chart(dfs['authors']),
            'genre_chart': viz.generate_genre_chart(dfs['genres']),
            'sales_chart': viz.generate_sales_chart(dfs['sales']),
            'customer_chart': viz.generate_customer_chart(dfs['customers']),
            'stock_chart': viz.generate_stock_chart(dfs['stock']),
            'publisher_chart': viz.generate_publisher_chart(dfs['publishers'])
        }
        cached_payload = {'charts': charts, 'stats': stats}
        cache.set(cache_key, cached_payload, 30)

    return render(request, 'Interfaces/admin_stats.html', {
        'charts': cached_payload['charts'],
        'stats': cached_payload['stats'],
        'filters': filters
    })

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
    if request.method != 'POST':
        return redirect('book_detail', pk=pk)

    uow = UnitOfWork()
    book = uow.books.get_by_id(pk)
    if not book:
        raise Http404("Книгу не знайдено")

    # Отримуємо кількість з форми (за замовчуванням 1)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    unit_price = 150.00
    total_price = unit_price * quantity

    profile = request.user.userprofile

    # Перевіряємо баланс на повну суму
    if profile.balance < total_price:
        return render(request, 'Interfaces/order_error.html', {
            'message': f'Недостатньо коштів! Потрібно {total_price} грн, а у вас {profile.balance} грн.'
        })

    # Логіка створення клієнта (якщо немає)
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
        # Створюємо замовлення
        order_data = {
            'customerid': customer,
            'orderdate': timezone.now(),
            'totalamount': total_price, # Записуємо загальну суму
            'paymentstatus': 'Paid'
        }
        order = uow.orders.create(order_data)

        # Створюємо деталі замовлення з кількістю
        Bookorderitem.objects.create(
            orderid=order,
            bookid=book,
            quantity=quantity, # <--- Важливо: записуємо обрану кількість
            unitprice=unit_price
        )

        # Знімаємо гроші
        profile.balance = float(profile.balance) - total_price
        profile.save()

    return redirect('my_orders')


@login_required
def my_orders(request):
    uow = UnitOfWork()
    email = request.user.email or f"{request.user.username}@example.com"
    orders = uow.orders.get_by_email(email)


    return render(request, 'Interfaces/my_orders.html', {'orders': orders})


@login_required
def admin_stats_concurrency(request):

    if not request.user.is_superuser:
        return redirect('index')

    service = ConcurrencyService()

    total_requests = int(request.GET.get('requests', 150))
    results = service.run_experiment(total_requests=total_requests)

    # Генеруємо графік
    viz = PlotlyVisualizationService()
    chart = viz.generate_concurrency_chart(results)

    return render(request, 'Interfaces/admin_stats_concurrency.html', {
        'chart': chart,
        'results': results,
        'total_requests': total_requests
    })
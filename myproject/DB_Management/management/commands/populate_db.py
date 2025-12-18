import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from DB_Management.models import (
    Author, Publisher, Book, Bookedition, Warehouse,
    Customer, Bookorder, Bookorderitem, Warehousestock
)


class Command(BaseCommand):
    help = 'Генерує реалістичні дані для бази MySQL без дублікатів'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=500, help='Кількість замовлень')

    def handle(self, *args, **options):
        total_orders = options['total']
        fake = Faker(['uk_UA'])
        self.stdout.write(self.style.WARNING(f'Починаємо наповнення MySQL (виправлення дублікатів)...'))

        with transaction.atomic():
            # 1. Створюємо Авторів (Author)
            authors_data = []
            for _ in range(30):
                authors_data.append(Author(
                    firstname=fake.first_name(),
                    lastname=fake.last_name(),
                    birthdate=fake.date_of_birth(minimum_age=25, maximum_age=80),
                    nationality=fake.country(),
                    biography=fake.text(max_nb_chars=200)
                ))
            Author.objects.bulk_create(authors_data, ignore_conflicts=True)
            authors = list(Author.objects.all())

            # 2. Створюємо Видавців (Publisher)
            publishers_data = []
            for _ in range(10):
                publishers_data.append(Publisher(
                    name=fake.unique.company(),
                    address=fake.street_address(),
                    city=fake.city(),
                    country="Україна",
                    contactemail=fake.company_email(),
                    phonenumber=fake.phone_number()
                ))
            Publisher.objects.bulk_create(publishers_data, ignore_conflicts=True)
            publishers = list(Publisher.objects.all())

            # 3. Створюємо Книги (Book)
            books_data = []
            for _ in range(50):
                books_data.append(Book(
                    title=fake.catch_phrase(),
                    isbn=fake.unique.isbn13().replace('-', ''),
                    publicationyear=random.randint(1990, 2024),
                    genre=random.choice(['Роман', 'Фантастика', 'Детектив', 'Драма']),
                    language='Українська',
                    authorid=random.choice(authors),
                    publisherid=random.choice(publishers)
                ))
            Book.objects.bulk_create(books_data, ignore_conflicts=True)
            books = list(Book.objects.all())

            # 4. Створюємо Видання (Bookedition)
            editions_data = []
            for book in books:
                for i in range(1, 3):
                    editions_data.append(Bookedition(
                        bookid=book,
                        editionnumber=i,
                        printrun=random.randint(500, 5000),
                        releasedate=fake.date_this_decade()
                    ))
            Bookedition.objects.bulk_create(editions_data, ignore_conflicts=True)
            editions = list(Bookedition.objects.all())

            # 5. Склади (Warehouse)
            warehouses_data = []
            locations = ['Київ', 'Львів', 'Одеса', 'Харків']
            for loc in locations:
                warehouses_data.append(Warehouse(
                    location=f"{loc}, {fake.street_address()}",
                    capacity=random.randint(10000, 50000),
                    managername=fake.name()
                ))
            Warehouse.objects.bulk_create(warehouses_data, ignore_conflicts=True)
            warehouses = list(Warehouse.objects.all())

            # 6. Клієнти (Customer)
            customers_data = []
            for _ in range(100):
                customers_data.append(Customer(
                    firstname=fake.first_name(),
                    lastname=fake.last_name(),
                    email=fake.unique.email(),
                    phonenumber=fake.phone_number(),
                    address=fake.address()
                ))
            Customer.objects.bulk_create(customers_data, ignore_conflicts=True)
            customers = list(Customer.objects.all())

            # 7. Замовлення (Bookorder)
            orders_to_create = []
            for _ in range(total_orders):
                orders_to_create.append(Bookorder(
                    customerid=random.choice(customers),
                    orderdate=fake.date_time_this_year(tzinfo=timezone.get_current_timezone()),
                    totalamount=0,
                    paymentstatus=random.choice(['Paid', 'Pending', 'Cancelled'])
                ))
            Bookorder.objects.bulk_create(orders_to_create)

            # Отримуємо замовлення для наповнення товарами
            new_orders = list(Bookorder.objects.order_by('-orderid')[:total_orders])

            # 8. Елементи замовлення (Bookorderitem) - ГАРАНТІЯ УНІКАЛЬНОСТІ КНИГ
            items_data = []
            for order in new_orders:
                order_total = 0
                num_items = random.randint(1, 3)
                # Використовуємо sample щоб уникнути дублікатів книг в одному замовленні
                selected_books = random.sample(books, k=num_items)

                for book in selected_books:
                    price = random.randint(250, 900)
                    qty = random.randint(1, 2)
                    order_total += price * qty
                    items_data.append(Bookorderitem(
                        orderid=order,
                        bookid=book,
                        quantity=qty,
                        unitprice=price
                    ))
                order.totalamount = order_total

            Bookorderitem.objects.bulk_create(items_data)
            Bookorder.objects.bulk_update(new_orders, ['totalamount'])

            # 9. Залишки (Warehousestock)
            stocks_data = []
            for warehouse in warehouses:
                selected_editions = random.sample(editions, k=min(len(editions), 20))
                for edition in selected_editions:
                    stocks_data.append(Warehousestock(
                        warehouseid=warehouse,
                        editionid=edition,
                        quantity=random.randint(5, 1000),
                        lastupdated=timezone.now()
                    ))
            Warehousestock.objects.bulk_create(stocks_data, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'Успішно! Створено {total_orders} замовлень без помилок цілісності.'))
from django.core.management.base import BaseCommand
from DB_Management.repositories.unit_of_work import UnitOfWork
import datetime


# -------------------------------------------------------------------
# ВАШОМУ ФАЙЛУ БРАКУВАЛО ОСЬ ЦІЄЇ СТРУКТУРИ:
#
# vvv  Клас ПОВИНЕН називатися 'Command' vvv
class Command(BaseCommand):
    # 'help' - це опис, який буде показано, якщо викличете 'python manage.py help demo_repository'
    help = 'Демонструє роботу патерну "Репозиторій" для Author, Publisher та Book.'

    # А ваша функція 'handle' має бути МЕТОДОМ цього класу
    def handle(self, *args, **options):
        # -----------------------------------------------------------

        # 'self.stdout' - це спосіб виводу в консоль для management команд
        self.stdout.write(self.style.SUCCESS('--- Початок Демонстрації Репозиторія ---'))

        # 1. Створюємо екземпляр UnitOfWork
        uow = UnitOfWork()

        # --- ДЕМОНСТРАЦІЯ 1: Author ---
        self.stdout.write(self.style.WARNING('\n--- Демо Автор (Author) ---'))

        # 2. Створення Автора
        author_data = {
            'firstname': 'Ліна',
            'lastname': 'Костенко',
            'birthdate': datetime.date(1930, 3, 19),
            'nationality': 'Українка'
        }
        try:
            new_author = uow.authors.create(author_data)
            self.stdout.write(self.style.SUCCESS(
                f'Створено: {new_author.firstname} {new_author.lastname} (ID: {new_author.authorid})'))

            # 3. Отримання по ID
            found_author = uow.authors.get_by_id(new_author.authorid)
            self.stdout.write(f'Знайдено по ID: {found_author.firstname}')

            # Зберігаємо для наступного кроку
            author_instance = new_author

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка при роботі з Author: {e}'))
            author_instance = None  # Не вдалося створити

        # --- ДЕМОНСТРАЦІЯ 2: Publisher ---
        self.stdout.write(self.style.WARNING('\n--- Демо Видавець (Publisher) ---'))

        # 4. Створення Видавця
        publisher_data = {
            'name': 'А-БА-БА-ГА-ЛА-МА-ГА',
            'city': 'Київ',
            'country': 'Україна'
        }
        try:
            new_publisher = uow.publishers.create(publisher_data)
            self.stdout.write(self.style.SUCCESS(f'Створено: {new_publisher.name} (ID: {new_publisher.publisherid})'))

            # 5. Отримання Всіх (перші 5)
            all_publishers = uow.publishers.get_all()
            self.stdout.write(f'Знайдено {all_publishers.count()} видавців (показуємо перші 5):')
            for pub in all_publishers[:5]:
                self.stdout.write(f'  - {pub.name}')

            # Зберігаємо для наступного кроку
            publisher_instance = new_publisher

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка при роботі з Publisher: {e}'))
            publisher_instance = None  # Не вдалося створити

        # --- ДЕМОНСТРАЦІЯ 3: Book ---
        self.stdout.write(self.style.WARNING('\n--- Демо Книга (Book) ---'))

        # 6. Створення Книги (з використанням ForeignKey)
        # Нам потрібні екземпляри author_instance та publisher_instance
        if author_instance and publisher_instance:
            book_data = {
                'title': 'Триста поезій. Вибране',
                'isbn': '9786175850367',
                'publicationyear': '2012',
                'genre': 'Поезія',
                'language': 'Українська',
                'authorid': author_instance,  # <--- Передаємо екземпляр
                'publisherid': publisher_instance  # <--- Передаємо екземпляр
            }
            try:
                new_book = uow.books.create(book_data)
                self.stdout.write(self.style.SUCCESS(f'Створено книгу: {new_book.title} (ID: {new_book.bookid})'))

                # 7. Перевірка
                found_book = uow.books.get_by_id(new_book.bookid)
                self.stdout.write(f'Знайдена книга: {found_book.title}')
                self.stdout.write(f'   -> Автор: {found_book.authorid.firstname} {found_book.authorid.lastname}')
                self.stdout.write(f'   -> Видавець: {found_book.publisherid.name}')

            except Exception as e:
                # Додаємо виведення детальної помилки, це важливо
                self.stdout.write(self.style.ERROR(f'Помилка при створенні Книги: {e}'))
                import traceback
                traceback.print_exc()
        else:
            self.stdout.write(
                self.style.ERROR('Не вдалося створити книгу, оскільки не вдалося створити Автора або Видавця.'))

        self.stdout.write(self.style.SUCCESS('\n--- Демонстрація Завершена ---'))


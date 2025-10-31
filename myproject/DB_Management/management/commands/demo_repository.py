from django.core.management.base import BaseCommand
from DB_Management.repositories.unit_of_work import UnitOfWork
import datetime

class Command(BaseCommand):
    help = 'Демонструє роботу патерну "Репозиторій" для Author, Publisher та Book.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Початок Демонстрації Репозиторія ---'))

        uow = UnitOfWork()

        self.stdout.write(self.style.WARNING('\n--- Демо Автор (Author) ---'))

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

            found_author = uow.authors.get_by_id(new_author.authorid)
            self.stdout.write(f'Знайдено по ID: {found_author.firstname}')

            author_instance = new_author

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка при роботі з Author: {e}'))
            author_instance = None

        self.stdout.write(self.style.WARNING('\n--- Демо Видавець (Publisher) ---'))

        publisher_data = {
            'name': 'А-БА-БА-ГА-ЛА-МА-ГА',
            'city': 'Київ',
            'country': 'Україна'
        }
        try:
            new_publisher = uow.publishers.create(publisher_data)
            self.stdout.write(self.style.SUCCESS(f'Створено: {new_publisher.name} (ID: {new_publisher.publisherid})'))

            all_publishers = uow.publishers.get_all()
            self.stdout.write(f'Знайдено {all_publishers.count()} видавців (показуємо перші 5):')
            for pub in all_publishers[:5]:
                self.stdout.write(f'  - {pub.name}')

            publisher_instance = new_publisher

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Помилка при роботі з Publisher: {e}'))
            publisher_instance = None

        self.stdout.write(self.style.WARNING('\n--- Демо Книга (Book) ---'))

        if author_instance and publisher_instance:
            book_data = {
                'title': 'Триста поезій. Вибране',
                'isbn': '9786175850367',
                'publicationyear': '2012',
                'genre': 'Поезія',
                'language': 'Українська',
                'authorid': author_instance,
                'publisherid': publisher_instance
            }
            try:
                new_book = uow.books.create(book_data)
                self.stdout.write(self.style.SUCCESS(f'Створено книгу: {new_book.title} (ID: {new_book.bookid})'))

                found_book = uow.books.get_by_id(new_book.bookid)
                self.stdout.write(f'Знайдена книга: {found_book.title}')
                self.stdout.write(f'   -> Автор: {found_book.authorid.firstname} {found_book.authorid.lastname}')
                self.stdout.write(f'   -> Видавець: {found_book.publisherid.name}')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Помилка при створенні Книги: {e}'))
                import traceback
                traceback.print_exc()
        else:
            self.stdout.write(
                self.style.ERROR('Не вдалося створити книгу, оскільки не вдалося створити Автора або Видавця.'))

        self.stdout.write(self.style.SUCCESS('\n--- Демонстрація Завершена ---'))
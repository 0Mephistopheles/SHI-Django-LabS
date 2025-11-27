from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from DB_Management.repositories.unit_of_work import UnitOfWork
from .forms import BookForm


# 1. Список книг (List View)
def book_list(request):
    uow = UnitOfWork()
    # Використовуємо репозиторій для отримання всіх записів
    books = uow.books.get_all()
    return render(request, 'Interfaces/book_list.html', {'books': books})


# 2. Деталі книги (Detail View)
def book_detail(request, pk):
    uow = UnitOfWork()
    # Отримуємо об'єкт по ID через репозиторій
    book = uow.books.get_by_id(pk)

    if not book:
        raise Http404("Книгу не знайдено")

    return render(request, 'Interfaces/book_detail.html', {'book': book})


# 3. Створення та Редагування (Create/Update View)
def book_form(request, pk=None):
    uow = UnitOfWork()
    book = None
    title = "Додавання нової книги"

    # Якщо передано pk, намагаємось знайти книгу для редагування
    if pk:
        book = uow.books.get_by_id(pk)
        if not book:
            raise Http404("Книгу не знайдено")
        title = "Редагування книги"

    if request.method == 'POST':
        # Передаємо instance=book, щоб форма знала, що ми (можливо) редагуємо цей об'єкт
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            # ! ВАЖЛИВО: Ми не використовуємо form.save(), бо це обхід UOW.
            # Ми беремо чисті дані з форми і передаємо їх у репозиторій.
            data = form.cleaned_data

            if pk:
                # Викликаємо метод update з репозиторія
                uow.books.update(pk, data)
            else:
                # Викликаємо метод create з репозиторія
                uow.books.create(data)

            return redirect('book_list')
    else:
        # GET запит: просто відображаємо форму (пусту або заповнену даними книги)
        form = BookForm(instance=book)

    return render(request, 'Interfaces/book_form.html', {'form': form, 'title': title})


# 4. Видалення (Delete View)
def book_delete(request, pk):
    uow = UnitOfWork()

    # Спочатку шукаємо книгу, щоб переконатись, що вона існує,
    # і щоб показати її назву на сторінці підтвердження.
    book = uow.books.get_by_id(pk)
    if not book:
        raise Http404("Книгу не знайдено")

    if request.method == 'POST':
        # Виконуємо видалення через репозиторій
        uow.books.delete_by_id(pk)
        return redirect('book_list')

    # Якщо GET - показуємо сторінку підтвердження
    return render(request, 'Interfaces/book_confirm_delete.html', {'book': book})
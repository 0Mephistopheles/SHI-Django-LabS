import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace with your settings module
django.setup()

from DB_Management.repositories.unit_of_work import UnitOfWork

def main():
    uow = UnitOfWork()

    while True:
        print("\nAdmin Panel")
        print("1. Create Author")
        print("2. List Authors")
        print("3. Create Publisher")
        print("4. List Publishers")
        print("5. Create Book")
        print("6. List Books")
        print("7. Delete by Id")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            firstname = input("First name: ")
            lastname = input("Last name: ")
            birthdate = input("Birthdate (YYYY-MM-DD): ")
            nationality = input("Nationality: ")
            data = {
                'firstname': firstname,
                'lastname': lastname,
                'birthdate': datetime.datetime.strptime(birthdate, "%Y-%m-%d").date(),
                'nationality': nationality
            }
            author = uow.authors.create(data)
            print(f"Created Author: {author.firstname} {author.lastname} (ID: {author.authorid})")

        elif choice == '2':
            authors = uow.authors.get_all()
            for a in authors:
                print(f"👤 {a.authorid}: {a.firstname} {a.lastname} ({a.nationality})")

        elif choice == '3':
            name = input("Publisher name: ")
            city = input("City: ")
            country = input("Country: ")
            data = {'name': name, 'city': city, 'country': country}
            pub = uow.publishers.create(data)
            print(f"Created Publisher: {pub.name} (ID: {pub.publisherid})")

        elif choice == '4':
            pubs = uow.publishers.get_all()
            for p in pubs:
                print(f"{p.publisherid}: {p.name} ({p.city}, {p.country})")

        elif choice == '5':
            title = input("Book title: ")
            isbn = input("ISBN: ")
            year = input("Publication year: ")
            genre = input("Genre: ")
            language = input("Language: ")
            author_id = int(input("Author ID: "))
            publisher_id = int(input("Publisher ID: "))
            author = uow.authors.get_by_id(author_id)
            publisher = uow.publishers.get_by_id(publisher_id)
            if author and publisher:
                data = {
                    'title': title,
                    'isbn': isbn,
                    'publicationyear': year,
                    'genre': genre,
                    'language': language,
                    'authorid': author,
                    'publisherid': publisher
                }
                book = uow.books.create(data)
                print(f" Created Book: {book.title} (ID: {book.bookid})")
            else:
                print("Invalid author or publisher ID.")

        elif choice == '6':
            books = uow.books.get_all()
            for b in books:
                print(f"{b.bookid}: {b.title} ({b.publicationyear}) — {b.authorid.firstname} / {b.publisherid.name}")

        elif choice == '7':
            author_id = int(input("Введіть ID автора для видалення: "))
            success = uow.authors.delete_by_id(author_id)
            if success:
                print("Автор успішно видалений.")
            else:
                print("Автор з таким ID не знайдений.")

        elif choice == '0':
            print("Exiting.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
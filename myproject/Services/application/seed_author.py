from Services.generator.author.author_generator import AuthorGenerator
from DB_Management.repositories.unit_of_work import UnitOfWork


def seed_authors(count: int):
    with UnitOfWork() as uow:
        for author_data in AuthorGenerator.generate_many(count):
            uow.authors.create(author_data)

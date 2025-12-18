from Services.generator.author.author_generator import AuthorGenerator
from DB_Management.repositories.unit_of_work import UnitOfWork

def seed_authors(count: int):
    with UnitOfWork() as uow:
        for row in AuthorGenerator.generate_many(count):
            uow.authors.create(row)

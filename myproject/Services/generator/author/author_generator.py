import random
from datetime import date
class AuthorGenerator:

from Services.generator.author.author_data import (
FIRST_NAMES,
LAST_NAMES,
NATIONALITIES,
CAPACITY_RANGE,
    )
    @staticmethod
    def _random_birth_date() -> str:
        year = random.randint(*BIRTH_YEAR_RANGE)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return date(year, month, day).isoformat()

    @staticmethod
    def _random_biography() -> str:
        return "This is a placeholder biography."

    @staticmethod
    def generate_one() -> dict:
        return {
            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES),
            "birth_date": AuthorGenerator._random_birth_date(),
            "nationality": random.choice(NATIONALITIES),
            "biography": AuthorGenerator._random_biography(),
        }

    @staticmethod
    def generate_many(count: int) -> list[dict]:
        return [AuthorGenerator.generate_one() for _ in range(count)]

import random
from datetime import date
import calendar
from Services.generator.author.author_data import (
    FIRST_NAMES,
    LAST_NAMES,
    NATIONALITIES,
    BIRTH_YEAR_RANGE,  # Add this
)

class AuthorGenerator:

    @staticmethod
    def _random_birthdate() -> date:
        year = random.randint(*BIRTH_YEAR_RANGE)
        month = random.randint(1, 12)
        # Use calendar.monthrange to find the last valid day of the specific month/year
        last_day = calendar.monthrange(year, month)[1]
        day = random.randint(1, last_day)
        return date(year, month, day)

    @staticmethod
    def _random_biography() -> str:
        # Placeholder biography text, you can improve this or use some lorem ipsum generator
        return "This author is well known for their remarkable contributions to literature."

    @staticmethod
    def generate_one() -> dict:
        return {
            "firstname": random.choice(FIRST_NAMES),
            "lastname": random.choice(LAST_NAMES),
            "birthdate": AuthorGenerator._random_birthdate(),
            "nationality": random.choice(NATIONALITIES),
            "biography": AuthorGenerator._random_biography(),
        }

    @staticmethod
    def generate_many(count: int) -> list[dict]:
        return [AuthorGenerator.generate_one() for _ in range(count)]

# services/generator/warehouse_generator.py
import random
from .warehouse_data import (
    LOCATIONS,
    FIRST_NAMES,
    LAST_NAMES,
    CAPACITY_RANGE,
)


class WarehouseGenerator:

    @staticmethod
    def _generate_manager_name() -> str:
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        return f"{first} {last}"

    @staticmethod
    def generate_one() -> dict:
        return {
            "location": random.choice(LOCATIONS),
            "capacity": random.randint(*CAPACITY_RANGE),
            "managername": WarehouseGenerator._generate_manager_name(),
        }

    @staticmethod
    def generate_many(count: int) -> list[dict]:
        return [WarehouseGenerator.generate_one() for _ in range(count)]

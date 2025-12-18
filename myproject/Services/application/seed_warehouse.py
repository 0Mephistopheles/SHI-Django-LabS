from myproject.Services.generator.warehouse.warehouse_generator import WarehouseGenerator
from myproject.DB_Management.repositories.unit_of_work import UnitOfWork


def seed_warehouses(count: int):
    with UnitOfWork() as uow:
        for row in WarehouseGenerator.generate_many(count):
            uow.warehouses.create(row)

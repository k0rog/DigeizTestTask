from injector import inject

from api.repositories.unit import UnitRepository
from api.models.unit import Unit


class UnitService:
    @inject
    def __init__(
        self,
        unit_repository: UnitRepository
    ):
        self._unit_repository = unit_repository

    def create(self, data: dict) -> Unit:
        return self._unit_repository.create(data)

    def bulk_create(self, data: dict) -> None:
        return self._unit_repository.bulk_create(data)

    def get_list(self, page: int, per_page: int) -> dict:
        return self._unit_repository.get_list(page, per_page)

    def get(self, unit_id: int) -> Unit:
        return self._unit_repository.get(unit_id)

    def update(self, unit_id: int, data: dict) -> bool:
        return self._unit_repository.update(unit_id, data)

    def delete(self, unit_id: int) -> bool:
        return self._unit_repository.delete(unit_id)

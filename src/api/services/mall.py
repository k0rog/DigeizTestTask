from injector import inject

from api.repositories.mall import MallRepository
from api.models.mall import Mall


class MallService:
    @inject
    def __init__(
        self,
        mall_repository: MallRepository
    ):
        self._mall_repository = mall_repository

    def create(self, data: dict) -> Mall:
        return self._mall_repository.create(data)

    def get_list(self, page: int, per_page: int) -> dict:
        return self._mall_repository.get_list(page, per_page)

    def get(self, mall_id: int) -> Mall:
        return self._mall_repository.get(mall_id)

    def update(self, mall_id: int, data: dict) -> bool:
        return self._mall_repository.update(mall_id, data)

    def delete(self, mall_id: int) -> bool:
        return self._mall_repository.delete(mall_id)

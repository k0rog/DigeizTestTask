from injector import inject

from api.repositories.account import AccountRepository
from api.models.account import Account


class AccountService:
    @inject
    def __init__(
        self,
        account_repository: AccountRepository
    ):
        self._account_repository = account_repository

    def create(self, data: dict) -> Account:
        return self._account_repository.create(data)

    def bulk_create(self, data: dict) -> None:
        return self._account_repository.bulk_create(data)

    def get_list(self, page: int, per_page: int) -> dict:
        return self._account_repository.get_list(page, per_page)

    def get(self, account_id: int) -> Account:
        return self._account_repository.get(account_id)

    def update(self, account_id: int, data: dict) -> bool:
        return self._account_repository.update(account_id, data)

    def delete(self, account_id: int) -> bool:
        return self._account_repository.delete(account_id)

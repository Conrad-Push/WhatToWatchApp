from abc import ABC, abstractmethod
from WTW_app.postgreSQL.database.schema import (
    DataGenerationResponse,
    DataScrappingResponse,
    DatabaseInfoResponse,
)


class IDatabaseRepository(ABC):
    @abstractmethod
    def check_database_status(self) -> DatabaseInfoResponse:
        pass

    @abstractmethod
    def restart_tables(self) -> DatabaseInfoResponse:
        pass

    @abstractmethod
    def generate_data(
        self,
        *,
        data_amount: int,
    ) -> DataGenerationResponse:
        pass

    @abstractmethod
    def scrap_data(
        self,
        *,
        data_amount: int,
    ) -> DataScrappingResponse:
        pass

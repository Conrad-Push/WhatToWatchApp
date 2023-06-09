from abc import ABC, abstractmethod
from WTW_app.database.schema import (
    DataGenerationResponse,
    DataScrappingResponse,
    DatabaseInfoResponse,
    TablesInfoResponse,
)


class IDatabaseRepository(ABC):
    @abstractmethod
    def check_database_status(self) -> DatabaseInfoResponse:
        pass

    @abstractmethod
    def get_tables_info(self) -> TablesInfoResponse:
        pass

    @abstractmethod
    def restart_tables(self) -> TablesInfoResponse:
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

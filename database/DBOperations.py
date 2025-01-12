from abc import ABC, abstractmethod

class DBOperations(ABC):
    @abstractmethod
    def insert(self, table: str, columns: list, values: list):
        pass

    @abstractmethod
    def delete(self, table: str, condition: str):
        pass

    @abstractmethod
    def update(self, table: str, set_values: dict, condition: str):
        pass

    @abstractmethod
    def select(self, table: str, columns: list, condition: str = None):
        pass
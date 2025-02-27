from typing import Optional
from abc import ABC, abstractmethod
from .providers.index import Provider

class SMS(ABC):
    @abstractmethod
    def send(self, phone_number: str, provider: Provider, otp: int):
        pass
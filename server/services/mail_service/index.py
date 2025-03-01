from typing import Optional
from abc import ABC, abstractmethod
from .providers.index import Provider

class Mail(ABC):
    @abstractmethod
    async def send(self, recipient: str, provider: Provider, verification_link: Optional[str] = None, current_time: Optional[str] = None, account_settings_url: Optional[str] = None, reset_password_link: Optional[str] = None):
        pass
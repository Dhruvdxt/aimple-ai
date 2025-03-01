from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    async def send_mail(self, recipient: str, subject: dict, body: dict):
        pass
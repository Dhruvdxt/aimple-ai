from enum import Enum
from .mail_service.index import MailService, MailType, ProviderType as MProviderType
from .sms_service.index import SMSService, SMSType, ProviderType as SProviderType


class ServiceType(str, Enum):
    MAIL_SERVICE = "MAIL_SERVICE"
    SMS_SERVICE = "SMS_SERVICE"
    
map: dict[str, any] = {
    "MAIL_SERVICE": MailService(),
    "SMS_SERVICE": SMSService()
}
    

class ServiceFactory():
    def get(self, service_type: ServiceType):
        return map[service_type]
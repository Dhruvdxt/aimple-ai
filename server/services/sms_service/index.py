from enum import Enum
from .sms_sender import SMSSender, ProviderType
# from .otp import OTP
# from .transection import TRANSECTION


class SMSType(str, Enum):
    OTP = "OTP"
    TRANSECTION = "TRANSECTION"
    
map: dict[str, any] = {
    # "OTP": OTP(),
    # "TRANSECTION": TRANSECTION()
}

class SMSService():
    def get_sms_sender(self):
        return SMSSender()
    
    def get(self, sms_type: SMSType):
        return map[sms_type]
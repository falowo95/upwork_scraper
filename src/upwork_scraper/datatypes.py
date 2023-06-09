import json
from dataclasses import dataclass
    
@dataclass
class JsonDataClass:

    def __str__(self):
        return str(self.to_json())
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, default=str)


@dataclass
class Address(JsonDataClass):
    city: str = None
    country: str = None
    line1: str = None
    line2: str = None
    postal_code: str = None
    state: str = None


@dataclass
class BasePay(JsonDataClass):
    amount: str = None
    period: str = None
    current: str = None


@dataclass
class PlatformIDs(JsonDataClass):
    employee_id: str = None
    position_id: str = None
    platform_user_id: str = None


@dataclass
class UpworkAccount(JsonDataClass):
    id: str = None
    account: str = None
    address: dict = None
    first_name: str = None
    last_name: str = None
    full_name: str = None
    birth_date: str = None
    email: str = None
    phone_number: str = None
    picture_url: str = None
    employment_status: str = None
    employment_type: str = None
    job_title: str = None
    ssn: str = None
    marital_status: str = None
    gender: str = None
    hire_date: str = None
    termination_date: str = None
    termination_reason: str = None
    employer: str = None
    base_pay: dict = None
    pay_cycle: str = 'monthly'
    platform_ids: dict = None
    created_at: str = None
    updated_at: str = None
    metadata: dict = None

    def merge(self, other):
        self.__dict__.update(other.__dict__)


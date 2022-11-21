from enum import Enum


class SubscriptionStatus(int, Enum):
    REQUESTED = 1
    CREATED = 2
    ERROR = 3

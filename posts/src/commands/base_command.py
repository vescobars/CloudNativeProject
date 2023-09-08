from abc import ABC, abstractmethod
import uuid


class BaseCommannd(ABC):
    @abstractmethod
    def execute(self):  # pragma: no cover
        raise NotImplementedError("Please implement in subclass")

    def is_uuid(self, string):
        try:
            uuid.UUID(string)
            return True
        except:
            return False

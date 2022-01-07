from enum import Enum
class Opcode(Enum):
    QUERY = 1

    Unknown = 16
    @classmethod
    def _missing_(cls, value: object):
        return Opcode.Unknown

class RCode(Enum):
    NoError = 0
    FormatError = 1
    ServerError = 2
    NameError = 3
    NotImplemented = 4
    Refused = 5

class RType(Enum):
    A = 1
    NS = 2
    CNAME = 5
    AAAA = 28

    Unknown = 256
    @classmethod
    def _missing_(cls, value: object):
        return RType.Unknown

# Because Python wont let me extend enums
class QType(Enum):
    A = 1
    NS = 2
    CNAME = 5
    AAAA = 28

    Unknown = 256
    @classmethod
    def _missing_(cls, value: object):
        return QType.Unknown

    All = 255


class RClass(Enum):
    IN = 1

    Unknown = 256
    @classmethod
    def _missing_(cls, value: object):
        return RClass.Unknown

class QClass(Enum):
    IN = 1

    Unknown = 256
    @classmethod
    def _missing_(cls, value: object):
        return QClass.Unknown

    All = 255
from abc import ABC
from ctypes import resize
import socket
import base64
import struct
from typing import List, Tuple, Union
from enums import *

class PrettyPrinter(object):
    def __str__(self):
        lines = [self.__class__.__name__ + ':']
        for key, val in vars(self).items():
            lines += '{}: {}'.format(key, val).split('\n')
        return '\n    '.join(lines)
    def __repr__(self) -> str:
        return self.__str__()

class Header(PrettyPrinter):
    id:int
    qr: bool
    opcode: Opcode
    aa: bool
    tc: bool
    rd: bool
    ra: bool
    Z: int
    rCode: RCode
    qdCount: int
    anCount: int
    nsCount: int
    arCount: int

    def __init__(self, id:int, qr: bool, opcode: Opcode, aa: bool, tc: bool, rd: bool, ra: bool, Z: int, rCode: RCode,  
                qdCount: int, anCount: int, nsCount: int, arCount: int) -> None:
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc=tc
        self.rd=rd
        self.ra=ra
        self.Z=Z
        self.rCode = rCode
        self.qdCount = qdCount
        self.anCount = anCount
        self.nsCount = nsCount
        self.arCount = arCount



class Question(PrettyPrinter):
    qName: str
    qType: QType
    qClass: QClass
    def __init__(self, qName, qType, qClass) -> None:
        self.qName = qName
        self.qType = qType
        self.qClass = qClass

class ARData(PrettyPrinter):
    ipAddress: str
    def __init__(self, ipAddress: str) -> None:
        self.ipAddress = ipAddress

class NSRData(PrettyPrinter):
    namespace: str
    def __init__(self, namespace: str) -> None:
        self.namespace = namespace
        
class CNameData(PrettyPrinter):
    alias: str
    def __init__(self, alias: str) -> None:
        self.alias = alias
        
class ResourceRecord(PrettyPrinter):
    name: str
    rtype: RType
    rclass: RClass
    ttl: int
    rdLength: int
    rData: Union[NSRData, ARData, CNameData]
    def __init__(self, name, rtype, rclass, ttl, rdLength, rData) -> None:
        self.name = name
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.rdLength = rdLength
        self.rData = rData
    
class Message(PrettyPrinter):
    header: Header
    questions: List[Question]
    answers: List[ResourceRecord]
    authority: List[ResourceRecord]
    additional: List[ResourceRecord]
    def __init__(self, header, questions, answers, authority, additional) -> None:
        self.header = header
        self.questions = questions
        self.answers = answers
        self.authority = authority
        self.additional = additional
        super().__init__()


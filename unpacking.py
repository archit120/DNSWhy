


from typing import Tuple
from enums import *
from structures import *
import struct

def read_string(data: bytes, start_pos: int) -> Tuple[str, int]:
    retstr = ''
    while True:
        length = data[start_pos]
        start_pos+=1
        if length == 0:
            return retstr[1:], start_pos
        elif length>63:
            length, = struct.unpack(">H", data[start_pos-1:start_pos+1])
            length -= 0xC000
            return (retstr+'.'+read_string(data, length)[0])[1:], start_pos+1
        retstr = retstr + '.' + data[start_pos:start_pos+length].decode('ascii')
        start_pos += length

def header_from_bytes(data: bytes):
    id, flags, qdCount, anCount, nsCount, \
        arCount = struct.unpack(">HHHHHH", data[:12])
    
    qr = ((flags & (1<<15))!=0)
    opcode = Opcode((flags >> 11)&0b1111)
    aa = ((flags & (1<<10))!=0)
    tc = ((flags & (1<<9))!=0)
    rd = ((flags & (1<<8))!=0)
    ra = ((flags & (1<<7))!=0)
    Z = (flags >> 4) &0b111
    assert(Z==0)
    rCode = RCode(flags & 0b1111)
    return Header(id, qr, opcode, aa, tc, rd, ra, Z, rCode, qdCount, anCount, nsCount, arCount)

def question_from_bytes(data: bytes, start_pos: int) -> Tuple[Question, int]:
    qName, start_pos = read_string(data, start_pos)
    qType, qClass = struct.unpack(">HH", data[start_pos:start_pos+4])
    return Question(qName, qType, qClass), start_pos+4

def arecord_from_bytes(data: bytes, start_pos: int) -> Tuple[ARData, int]:
    return ARData(socket.inet_ntoa(data[start_pos: start_pos+4])), start_pos+4

def nsrecord_from_bytes(data: bytes, start_pos: int) -> Tuple[NSRData, int]:
    read, pos = read_string(data, start_pos)
    return NSRData(read), pos

def cnamerecord_from_bytes(data: bytes, start_pos: int) -> Tuple[CNameData, int]:
    read, pos = read_string(data, start_pos)
    return CNameData(read), pos

def resourcerecord_from_bytes(data: bytes, start_pos: int) -> Tuple[ResourceRecord, int]:
    name, start_pos = read_string(data, start_pos)
    rtype, rclass, ttl, RDLength = struct.unpack(">HHIH", data[start_pos:start_pos+10])
    if rtype == 2:
        RData = nsrecord_from_bytes(data, start_pos+10)[0]
    elif rtype == 1:
        RData = arecord_from_bytes(data, start_pos+10)[0]
    elif rtype == 5:
        RData = cnamerecord_from_bytes(data, start_pos+10)[0]
    else:
        if rtype != 28: #Do not warn about AAAA (ipv6) records
            print("Unknown record type with rtype: {0}. Data will be ignored".format(rtype))
        RData = None
    end_pos = start_pos+10+RDLength
    rtype = RType(rtype)
    rclass = RClass(rclass)
    return ResourceRecord(name, rtype, rclass, ttl, RDLength, RData), end_pos

def message_from_bytes(data: bytes) -> Message:
    header = header_from_bytes(data)
    questions = []
    answers = []
    authority = []
    additional = []
    start_pos = 12
    for _ in range(header.qdCount):
        question, start_pos = question_from_bytes(data, start_pos)
        questions.append(question)
    for _ in range(header.anCount):
        rr, start_pos = resourcerecord_from_bytes(data, start_pos)
        answers.append(rr)
    for _ in range(header.nsCount):
        rr, start_pos = resourcerecord_from_bytes(data, start_pos)
        authority.append(rr)
    for _ in range(header.arCount):
        rr, start_pos = resourcerecord_from_bytes(data, start_pos)
        additional.append(rr)
    
    return Message(header, questions, answers, authority, additional)

if __name__ == "__main__":
    server = "198.41.0.4"
    port = 53

    message_hex = "010000000001000000000000076369746164656C03636F6D0000010001"
    message_binary = base64.b16decode(message_hex, True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message_binary, (server, port))
    data_orig, _ = sock.recvfrom(1024)


    msg = message_from_bytes(data_orig)
    print(msg)
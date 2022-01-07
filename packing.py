from structures import *

def write_string(string: str) -> bytearray:
    parts = string.split('.')
    arr = bytearray()
    for part in parts:
        arr.append(len(part))
        arr.extend(part.encode('ascii'))
    arr.append(0)
    return arr

def question_to_bytes(question: Question, data: bytearray):
    data.extend(write_string(question.qName))
    data.extend(struct.pack(">HH", question.qType.value, question.qClass.value))

# Do we need these?

def arecord_to_bytes(aRData: ARData, data:bytearray):
    data.extend(socket.inet_aton(aRData.ipAddress))

def nsrecord_to_bytes(nsRData: NSRData, data: bytearray):
    data.extend(write_string(nsRData.namespace))

def header_to_bytes(header: Header, data: bytearray):
    flags = header.rCode | (header.Z<<4) | (header.ra<<7) \
         | (header.rd<<8) | (header.tc << 9) | (header.aa<<10) \
         | (header.opcode << 11) | (header.qr << 15)
    data.extend(struct.pack(">HHHHHH", header.id, flags, \
        header.qdCount, header.anCount, header.nsCount, \
        header.arCount))

def message_to_bytes(message: Message) -> bytes:
    data = bytearray()
    header_to_bytes(message.header, data)
    for question in message.questions:
        question_to_bytes(question, data)
    return bytes(data)

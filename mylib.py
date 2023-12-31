import struct
import codecs

def divide_four(option):
    if len(option) % 4 != 0:
        header_len = int(len(option) / 4) + 1
        return header_len
    else:
        header_len = int(len(option) / 4)
        return header_len

def add_x00(option):
    return (4 - (len(option) % 4)) * (str.encode('\x00'))

# 将十六进制字母转换为十进制
def from_hex_to_deci(character):
    if character == 'A' or character == 'a':
        return 10
    else:
        if character == 'B' or character == 'b':
            return 11
        else:
            if character == 'C' or character == 'c':
                return 12
            else:
                if character == 'D' or character == 'd':
                    return 13
                else:
                    if character == 'E' or character == 'e':
                        return 14
                    else:
                        if character == 'F' or character == 'f':
                            return 15
                        else:
                            if '0' <= character <= '9':
                                return int(character)
# convert string to bytes
def byte_transform(data):
    length = int(len(data) / 2)
    result = b''
    for i in range(length):
        substr = data[i * 2: (i + 1) * 2]
        num_1 = from_hex_to_deci(substr[0])
        num_2 = from_hex_to_deci(substr[1])
        num = num_1 * 16 + num_2
        result += struct.pack("!B", num)
    return result

def data_process(data):
    if isinstance(data, bytes):
        return data
    else:
        return byte_transform(data)

def mac_process(mac_address):
    mac_address = mac_address.replace(':', '')
    return codecs.decode(mac_address, 'hex')

def reverse_mac_process(mac_address):
    n = bytes.decode(codecs.encode(mac_address, 'hex'))
    mac = ''
    for i in range(17):
        if (i + 1) % 3 == 0:
            mac += ':'
        else:
            mac += n[i - int(i / 3)]
    return mac
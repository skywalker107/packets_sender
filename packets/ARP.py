import socket
import struct
from mylib import mac_process

# IP报文类
class ARP_Packet:
    def __init__(self, arp_pack=None):
        if arp_pack is None:
            return
        # 硬件类型，一般为以太网
        self.hardware_type = 0x0001
        # 协议类型，一般为IP
        self.protocol_type = 0x0800
        # MAC地址长度
        self.hardware_length = 0x0006
        # IP地址长度
        self.protocol_length = 0x0004
        # 操作代码
        self.operation_code = arp_pack['operation_code']
        # 源MAC地址
        self.source_hardware_address = mac_process(arp_pack['source_hardware_address'])
        # 源IP地址
        self.source_protocol_address = socket.inet_aton(arp_pack['source_protocol_address'])
        # 目的MAC地址
        self.destination_hardware_address = mac_process(arp_pack['destination_hardware_address'])
        # 目的IP地址
        self.destination_protocol_address = socket.inet_aton(arp_pack['destination_protocol_address'])
        #
        if arp_pack['destination_hardware_address'] == '00:00:00:00:00:00':
            # convert mac address to bytes
            self.broadcast = mac_process('ff:ff:ff:ff:ff:ff')
        else:
            self.broadcast = mac_process(arp_pack['destination_hardware_address'])

    # 将ARP数据打包
    def pack(self):
        arp_pro = 0x0806  # 代表是ARP协议
        ether = struct.pack("!6s6sH", self.broadcast, self.source_hardware_address, arp_pro)

        arp = struct.pack("!HHBBH6s4s6s4s", self.hardware_type, self.protocol_type, self.hardware_length, self.protocol_length, self.operation_code,
                               self.source_hardware_address, self.source_protocol_address, self.destination_hardware_address, self.destination_protocol_address)
        # 完整的IP报文
        packet = ether + arp
        return packet

    # 发出IP包
    def send(self, my):
        sock_send = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock_send.bind((my, 0))
        sock_send.send(self.pack())
        sock_send.close()

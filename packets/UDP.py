import socket
import struct
from mylib import divide_four, add_x00, data_process


# UDP报文类
class UDP_Packet:
    def __init__(self, udp_pack=None):
        if udp_pack is None:
            return
        # 源端口
        self.source_port = udp_pack['source_port']
        # 目的端口
        self.destination_port = udp_pack['destination_port']
        # 总长度
        self.length = 8
        # 校验和
        self.check_sum = 0
        # 数据
        self.data = data_process(udp_pack['data'])
        # 重新计算总长度
        self.length = self.length + int(len(self.data))
        # 源IP地址
        self.source_address = socket.inet_aton(udp_pack['source_address'])
        # 目的IP地址
        self.destination_address = socket.inet_aton(udp_pack['destination_address'])

    # 计算头部校验和
    def check_sum_cal(self, before_check):
        length = len(before_check)
        check_sum = ~((before_check[0] << 8)+before_check[1]) & 0xFFFF
        for i in range(2, length, 2):
            num_final = check_sum + ~((before_check[i] << 8)+before_check[i+1]) & 0xFFFF
        return ~check_sum & 0xFFFF


    # 将UDP数据打包
    def pack(self):
        # 计算校验和之前的UDP报文
        before_check = struct.pack("!4s4sHHHHHH", self.source_address, self.destination_address, 17, self.length, self.source_port,
                               self.destination_port, self.length, 0)
        # 计算校验和
        self.check_sum = self.check_sum_cal(before_check)
        # 完整的UDP报文头部
        after_check = struct.pack("!4s4sHHHHHH", self.source_address, self.destination_address, 17, self.length, self.source_port,
                               self.destination_port, self.length, self.check_sum)
        # 完整的UDP报文
        packet = after_check + self.data
        return packet

    # 发出UDP包
    def send(self):
        #创建一个原始套接字，指定UDPv4地址族，使用TCP协议
        socket_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        #使用sendto方法发送经过封装的UDP数据包到指定目的端口
        socket_send.sendto(self.pack(), (socket.inet_ntoa(self.destination_address), self.destination_port))
        #关闭套接字
        socket_send.close()

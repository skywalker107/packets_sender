import socket
import struct
from mylib import divide_four, add_x00, data_process


# ICMP报文类
class ICMP_Packet:
    def __init__(self, icmp_pack=None):
        if icmp_pack is None:
            return
        # ICMP类型
        self.type = icmp_pack['type']
        # 代码
        self.code = 0
        # 校验和
        self.check_sum = 0
        # 标识
        self.id = icmp_pack['identification']
        #序列号
        self.sequence = icmp_pack['sequence']

    # 计算头部校验和
    def check_sum_cal(self, before_check):
        leng = len(before_check)
        check_sum = 0
        if leng % 2 == 0:
            for i in range(0, leng, 2):
                check_sum += (before_check[i] << 8) + before_check[i + 1]
        else:
            for i in range(0, leng - 1, 2):
                check_sum += (before_check[i] << 8) + before_check[i + 1]
            check_sum = check_sum + before_check[leng - 1]
        while check_sum >> 16:
            check_sum = (check_sum & 0xffff) + check_sum >> 16
        check_sum = (~check_sum) & 0xffff
        return check_sum

    # 将ICMP数据打包
    def pack(self):
        before_check = struct.pack("!BBHHH", self.type, self.code, self.check_sum, self.id, self.sequence)

        self.check_sum = self.check_sum_cal(before_check)

        after_check = struct.pack("!BBHHH", self.type, self.code, self.check_sum, self.id, self.sequence)

        return after_check

    # 发出ICMP包
    def send(self, destination_address):
        service = socket.getprotobyname("icmp")
        socket_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, service)
        socket_send.settimeout(3)
        try:
            socket_send.sendto(self.pack(), (socket.inet_aton(destination_address), 1))
            reply = socket_send.recvfrom(1024)
            if reply is not None:
                print(reply)
            socket_send.close()
        except:
            socket_send.close()

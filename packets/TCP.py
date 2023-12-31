import socket
import struct
from mylib import divide_four, add_x00, data_process

# TCP报文类
class TCP_Packet:
    def __init__(self, tcp_pack=None):
        if tcp_pack is None:
            return
        # 源端口
        self.source_port = tcp_pack['source_port']
        # 目的端口
        self.destination_port = tcp_pack['destination_port']
        # 源IP地址
        self.source_address = socket.inet_aton(tcp_pack['source_address'])
        # 目的IP地址
        self.destination_address = socket.inet_aton(tcp_pack['destination_address'])
        # 序列号
        self.sequence = tcp_pack['sequence']
        # 确认号
        self.acknowledge_num = tcp_pack['acknowledge_num']
        # 偏移
        self.data_offset = 5
        # 保留
        self.reserved = 0

        self.URG = tcp_pack['URG']
        self.ACK = tcp_pack['ACK']
        self.PSH = tcp_pack['PSH']
        self.RST = tcp_pack['SYN']
        self.FIN = tcp_pack['FIN']
        # 窗口
        self.window = tcp_pack['window']
        # 校验和（初始值为0）
        self.check_sum = 0
        # 紧急指针
        self.urg_point = tcp_pack['urg_point']
        if self.URG == 0:
            self.urg_point = 0
        # 可选项
        self.option = data_process(tcp_pack['option'])
        # 判断option可选项是否指明
        if self.option == '':
            # 如果不存在
            self.option = str.encode('')
        else:
            # 如果存在
            self.data_offset = self.data_offset + divide_four(self.option)
        # 对数据进行处理
        self.data = data_process(tcp_pack['data'])

    # 计算头部校验和
    def check_sum_cal(self, before_check):
        length = len(before_check)
        check_sum = 0
        # 分情况讨论头部长度为偶数和奇数
        if len(before_check) % 2 == 0:
            for i in range(0, length, 2):
                check_sum += (before_check[i] << 8) + before_check[i + 1]
        else:
            for i in range(0, length - 1, 2):
                check_sum += (before_check[i] << 8) + before_check[i + 1]
            check_sum += before_check[length - 1]
        # 确保校验和的计算结果在16位范围内
        while check_sum >> 16:
            check_sum = (check_sum & 0xffff) + check_sum >> 16
        check_sum = (~check_sum) & 0xffff
        return check_sum

    # 将IP数据打包
    def pack(self):
        con_flag = (self.data_offset << 12) + (self.URG << 5) + (self.ACK << 4) + (self.PSH << 3) + (self.RST << 2) + (self.PSH << 1) + (self.FIN)
        # 进行打包
        before_check = struct.pack("!HHLLHHHH", self.source_port, self.destination_port, self.sequence, self.acknowledge_num, con_flag,
                               self.window, self.check_sum, self.urg_point)

        if len(self.data) % 4 != 0:
            self.data = self.data + add_x00(self.data)

        pseudo_header = struct.pack("!4s4sHH", self.source_address, self.destination_address, 6, int(self.data_offset) * 4 + int(len(self.data)))

        if self.option != str.encode(''):
            self.check_sum = self.check_sum_cal(pseudo_header + before_check + self.option + self.data)
        else:
            self.check_sum = self.check_sum_cal(pseudo_header + before_check + self.data)

        tcp_head = struct.pack("!HHLLHHHH", self.source_port, self.destination_port, self.sequence, self.acknowledge_num, con_flag,
                               self.window, self.check_sum, self.urg_point)

        if self.option != str.encode(''):
            if len(self.option) % 4 == 0:
                # option长度已经是4的倍数，直接拼接
                tcp_head = tcp_head + self.option
            else:
                # option长度不是4的倍数，要添加x00
                tcp_head = tcp_head + self.option + add_x00(self.option)

        # 完整的IP报文
        packet = tcp_head + self.data
        return packet

    # 发出IP包
    def send(self):

        socket_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        socket_send.connect((socket.inet_ntoa(self.destination_address), self.destination_port))

        socket_send.sendto(self.pack(), (socket.inet_ntoa(self.destination_address), self.destination_port))

        socket_send.close()
import socket
import struct
from mylib import divide_four, add_x00, data_process

# IP报文类
class IP_Packet:
    def __init__(self, ip_pack=None):
        if ip_pack is None:
            return
        # ip版本为ipv4
        self.version = 4
        # 首部长度
        self.header_len = 5
        # 区分服务
        self.ds = ip_pack['ds']
        # 标识
        self.id = ip_pack['identification']
        # 标志
        self.flag = ip_pack['flag']
        # 片偏移
        self.frag_off = ip_pack['frag_off']
        # 生存时间
        self.ttl = ip_pack['time_to_live']
        # 协议
        self.protocol = ip_pack['protocol']
        # 头部校验和（初始值为0）
        self.header_check_sum = 0
        # 源IP地址
        self.source_address = socket.inet_aton(ip_pack['source_address'])
        # 目的IP地址
        self.destination_address = socket.inet_aton(ip_pack['destination_address'])
        # 可选项
        self.option = data_process(ip_pack['option'])
        # 判断option可选项是否指明
        if self.option == '':
            # 如果不存在
            self.option = str.encode('')
        else:
            # 如果存在
            self.header_len = self.header_len + divide_four(self.option)
        # 对数据进行处理
        self.data = data_process(ip_pack['data'])
        # 重新计算总长度
        self.total_len = self.header_len * 4 + int(len(self.data))

    # 计算头部校验和
    def check_sum_cal(self, header):
        length = len(header)
        check_sum = 0
        # 分情况讨论头部长度为偶数和奇数
        if len(header) % 2 == 0:
            for i in range(0, length, 2):
                check_sum += (header[i] << 8) + header[i + 1]
        else:
            for i in range(0, length - 1, 2):
                check_sum += (header[i] << 8) + header[i + 1]
            check_sum += header[length - 1]
        # 确保校验和的计算结果在16位范围内
        while check_sum >> 16:
            check_sum = (check_sum & 0xffff) + check_sum >> 16
        check_sum = (~check_sum) & 0xffff
        return check_sum

    # 将IP数据打包
    def pack(self):
        # 拼接ip版本号和首部长度
        version_header_len = (self.version << 4) + self.header_len
        # 拼接标志和片偏移
        flag_and_frag = (self.flag << 13) + self.frag_off
        # 进行打包
        before_check = struct.pack("!BBHHHBBH4s4s", version_header_len, self.ds, self.total_len, self.id, flag_and_frag,
                               self.ttl, self.protocol, self.header_check_sum, self.source_address,
                               self.destination_address)

        # 对可能存在的可选项option进行处理
        if self.option != str.encode(''):
            self.header_check_sum = self.check_sum_cal(before_check + self.option)
        else:
            self.header_check_sum = self.check_sum_cal(before_check)

        after_check = struct.pack("!BBHHHBBH4s4s", version_header_len, self.ds, self.total_len, self.id, flag_and_frag,
                               self.ttl, self.protocol, self.header_check_sum, self.source_address,
                               self.destination_address)

        if self.option != str.encode(''):
            if len(self.option) % 4 == 0:
                # option长度已经是4的倍数，直接拼接
                after_check = after_check + self.option
            else:
                # option长度不是4的倍数，要添加x00
                after_check = after_check + self.option + add_x00(self.option)

        # 完整的IP报文
        packet = after_check + self.data
        return packet

    # 发出IP包
    def send(self, destination_port):
        #创建一个原始套接字，指定IPv4地址族，使用TCP协议
        socket_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        #设置套接字选项，包括指定IP头部由用户程序自己构造
        socket_send.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        #使用sendto方法发送经过封装的IP数据包到指定目的端口
        socket_send.sendto(self.pack(), (socket.inet_ntoa(self.destination_address), destination_port))
        #关闭套接字
        socket_send.close()

from packets.ARP import ARP_Packet
from packets.ICMP import ICMP_Packet
from packets.IP import IP_Packet
from packets.TCP import TCP_Packet
from packets.UDP import UDP_Packet

import socket
import uuid
import os

OP_REQUEST = 0x0001
OP_REPLY = 0x0002

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class NetworkConfigWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="packets_sender")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = ''

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # 创建一个标签页容器
        notebook = Gtk.Notebook()
        scrolled_window.add(notebook)
        self.add(scrolled_window)

        # 创建IP标签页
        ip_tab = Gtk.Grid()
        ip_tab.set_border_width(3)

        # IP 参数文本框
        ds_label = Gtk.Label("ds:")

        self.ds_entry = Gtk.Entry()
        self.ds_entry.set_text("0")  # 默认为0


        ip_identification_label = Gtk.Label("identification:")

        self.ip_identification_entry = Gtk.Entry()
        self.ip_identification_entry.set_text("1")  # 默认为1




        df_label = Gtk.Label("DF:")

        self.df_entry = Gtk.Entry()
        self.df_entry.set_text("1")  # 默认为1


        mf_label = Gtk.Label("MF:")

        self.mf_entry = Gtk.Entry()
        self.mf_entry.set_text("0")  # 默认为0


        ip_frag_off_label = Gtk.Label("frag_off:")

        self.ip_frag_off_entry = Gtk.Entry()
        self.ip_frag_off_entry.set_text("0")  # 默认为0

        time_to_live_label = Gtk.Label("time_to_live:")

        self.time_to_live_entry = Gtk.Entry()
        self.time_to_live_entry.set_text("128")  # 默认为128



        ip_destination_port_label = Gtk.Label("destination_port:")

        self.ip_destination_port_entry = Gtk.Entry()


        ip_source_address_label = Gtk.Label("source_address:")

        self.ip_source_address_entry = Gtk.Entry()
        self.ip_source_address_entry.set_text(ip)


        ip_destination_address_label = Gtk.Label("destination_address:")

        self.ip_destination_address_entry = Gtk.Entry()


        ip_protocol_label = Gtk.Label("protocol:")

        self.ip_protocol_entry = Gtk.Entry()
        self.ip_protocol_entry.set_placeholder_text("TCP或UDP或ICMP")


        ip_option_label = Gtk.Label("option:")

        self.ip_option_entry = Gtk.Entry()
        self.ip_option_entry.set_placeholder_text("请输入16进制数字")  # 默认值


        ip_data_label = Gtk.Label("data:")

        self.ip_data_entry = Gtk.Entry()
        self.ip_data_entry.set_placeholder_text("请输入16进制数字")  # 默认值


        ip_send_button = Gtk.Button(label="Send")
        ip_send_button.connect("clicked", self.ip_sender)

        # 添加IP标签页到Notebook
        notebook.append_page(ip_tab, Gtk.Label("IP"))


        # 将标签和输入框添加到Grid中
        ip_tab.attach(ds_label, 0, 0, 1, 1)
        ip_tab.attach(self.ds_entry, 1, 0, 1, 1)

        ip_tab.attach(ip_identification_label, 2, 0, 1, 1)
        ip_tab.attach(self.ip_identification_entry, 3, 0, 1, 1)

        ip_tab.attach(df_label, 4, 0, 1, 1)
        ip_tab.attach(self.df_entry,5, 0, 1, 1)

        ip_tab.attach(mf_label, 0, 1, 1, 1)
        ip_tab.attach(self.mf_entry, 1, 1, 1, 1)

        ip_tab.attach(ip_frag_off_label, 2, 1, 1, 1)
        ip_tab.attach(self.ip_frag_off_entry, 3, 1, 1, 1)

        ip_tab.attach(time_to_live_label, 4, 1, 1, 1)
        ip_tab.attach(self.time_to_live_entry, 5, 1, 1, 1)

        ip_tab.attach(ip_destination_port_label, 0, 2, 1, 1)
        ip_tab.attach(self.ip_destination_port_entry, 1, 2, 1, 1)

        ip_tab.attach(ip_source_address_label, 2, 2, 1, 1)
        ip_tab.attach(self.ip_source_address_entry, 3, 2, 1, 1)

        ip_tab.attach(ip_destination_address_label, 4, 2, 1, 1)
        ip_tab.attach(self.ip_destination_address_entry, 5, 2, 1, 1)

        ip_tab.attach(ip_protocol_label, 0, 3, 1, 1)
        ip_tab.attach(self.ip_protocol_entry, 1, 3, 1, 1)

        ip_tab.attach(ip_option_label, 2, 3, 1, 1)
        ip_tab.attach(self.ip_option_entry, 3, 3, 1, 1)

        ip_tab.attach(ip_data_label, 4, 3, 1, 1)
        ip_tab.attach(self.ip_data_entry, 5, 3, 1, 1)

        ip_tab.attach(ip_send_button, 5, 4, 1, 1)








        # 创建TCP标签页
        tcp_tab = Gtk.Grid()
        tcp_tab.set_border_width(3)

        # TCP 参数文本框
        tcp_source_port_label = Gtk.Label("source_port:")
        self.tcp_source_port_entry = Gtk.Entry()
        self.tcp_source_port_entry.set_text("0")  # 默认为0

        tcp_destination_port_label = Gtk.Label("destination_port:")
        self.tcp_destination_port_entry = Gtk.Entry()
        self.tcp_destination_port_entry.set_text("0")  # 默认为0

        tcp_source_address_label = Gtk.Label("source_address:")
        self.tcp_source_address_entry = Gtk.Entry()
        self.tcp_source_address_entry.set_text(ip)

        tcp_destination_address_label = Gtk.Label("destination_address:")
        self.tcp_destination_address_entry = Gtk.Entry()
        self.tcp_destination_address_entry.set_text("0")  # 默认为0

        tcp_sequence_label = Gtk.Label("sequence:")
        self.tcp_sequence_entry = Gtk.Entry()
        self.tcp_sequence_entry.set_text("0")  # 默认为0

        acknowledge_num_label = Gtk.Label("acknowledge_num:")
        self.acknowledge_num_entry = Gtk.Entry()
        self.acknowledge_num_entry.set_text("0")  # 默认为0

        URG_label = Gtk.Label("URG:")
        self.URG_entry = Gtk.Entry()
        self.URG_entry.set_text("0")  # 默认为0

        ACK_label = Gtk.Label("ACK:")
        self.ACK_entry = Gtk.Entry()
        self.ACK_entry.set_text("1")  # 默认为1

        PSH_label = Gtk.Label("PSH:")
        self.PSH_entry = Gtk.Entry()
        self.PSH_entry.set_text("0")  # 默认为0

        RST_label = Gtk.Label("RST:")
        self.RST_entry = Gtk.Entry()
        self.RST_entry.set_text("0")  # 默认为0

        SYN_label = Gtk.Label("SYN:")
        self.SYN_entry = Gtk.Entry()
        self.SYN_entry.set_text("0")  # 默认为0

        FIN_label = Gtk.Label("FIN:")
        self.FIN_entry = Gtk.Entry()
        self.FIN_entry.set_text("0")  # 默认为0

        window_label = Gtk.Label("window:")
        self.window_entry = Gtk.Entry()
        self.window_entry.set_text("1024")  # 默认为0

        urg_point_label = Gtk.Label("urg_point:")
        self.urg_point_entry = Gtk.Entry()
        self.urg_point_entry.set_text("0")  # 默认为0

        tcp_option_label = Gtk.Label("option:")
        self.tcp_option_entry = Gtk.Entry()
        self.tcp_option_entry.set_placeholder_text("请输入16进制数字")  # 默认为0

        tcp_data_label = Gtk.Label("data:")
        self.tcp_data_entry = Gtk.Entry()
        self.tcp_data_entry.set_placeholder_text("请输入16进制数字")  # 默认为0

        tcp_send_button = Gtk.Button(label="Send")
        tcp_send_button.connect("clicked", self.tcp_sender)

        # 添加TCP标签页到Notebook
        notebook.append_page(tcp_tab, Gtk.Label("TCP"))

        tcp_tab.attach(tcp_source_port_label, 0, 0, 1, 1)
        tcp_tab.attach(self.tcp_source_port_entry, 1, 0, 1, 1)

        tcp_tab.attach(tcp_destination_port_label, 2, 0, 1, 1)
        tcp_tab.attach(self.tcp_destination_port_entry, 3, 0, 1, 1)

        tcp_tab.attach(tcp_source_address_label, 4, 0, 1, 1)
        tcp_tab.attach(self.tcp_source_address_entry, 5, 0, 1, 1)

        tcp_tab.attach(tcp_destination_address_label, 0, 1, 1, 1)
        tcp_tab.attach(self.tcp_destination_address_entry,1, 1, 1, 1)

        tcp_tab.attach(tcp_sequence_label, 2, 1, 1, 1)
        tcp_tab.attach(self.tcp_sequence_entry, 3, 1, 1, 1)

        tcp_tab.attach(acknowledge_num_label, 4, 1, 1, 1)
        tcp_tab.attach(self.acknowledge_num_entry, 5, 1, 1, 1)

        tcp_tab.attach(URG_label, 0, 2, 1, 1)
        tcp_tab.attach(self.URG_entry, 1, 2, 1, 1)

        tcp_tab.attach(ACK_label, 2, 2, 1, 1)
        tcp_tab.attach(self.ACK_entry, 3, 2, 1, 1)

        tcp_tab.attach(PSH_label, 4, 2, 1, 1)
        tcp_tab.attach(self.PSH_entry, 5, 2, 1, 1)

        tcp_tab.attach(RST_label, 0, 3, 1, 1)
        tcp_tab.attach(self.RST_entry, 1, 3, 1, 1)

        tcp_tab.attach(SYN_label, 2, 3, 1, 1)
        tcp_tab.attach(self.SYN_entry, 3, 3, 1, 1)

        tcp_tab.attach(FIN_label, 4, 3, 1, 1)
        tcp_tab.attach(self.FIN_entry, 5, 3, 1, 1)

        tcp_tab.attach(window_label, 0, 4, 1, 1)
        tcp_tab.attach(self.window_entry, 1, 4, 1, 1)

        tcp_tab.attach(urg_point_label, 2, 4, 1, 1)
        tcp_tab.attach(self.urg_point_entry, 3, 4, 1, 1)

        tcp_tab.attach(tcp_option_label, 4, 4, 1, 1)
        tcp_tab.attach(self.tcp_option_entry, 5, 4, 1, 1)

        tcp_tab.attach(tcp_data_label, 0, 5, 1, 1)
        tcp_tab.attach(self.tcp_data_entry, 1, 5, 1, 1)

        tcp_tab.attach(tcp_send_button, 5, 5, 1, 1)

        # 创建UDP标签页
        udp_tab = Gtk.Grid()
        udp_tab.set_border_width(3)

        # UDP 参数文本框
        udp_source_port_label = Gtk.Label("source_port:")
        self.udp_source_port_entry = Gtk.Entry()
        self.udp_source_port_entry.set_text("0")  # 默认为0

        udp_destination_port_label = Gtk.Label("destination_port:")
        self.udp_destination_port_entry = Gtk.Entry()
        self.udp_destination_port_entry.set_text("0")  # 默认为0

        udp_data_label = Gtk.Label("data:")
        self.udp_data_entry = Gtk.Entry()
        self.udp_data_entry.set_placeholder_text("请输入16进制数字")  # 默认为0

        udp_source_address_label = Gtk.Label("source_address:")
        self.udp_source_address_entry = Gtk.Entry()
        self.udp_source_address_entry.set_text(ip)

        udp_destination_address_label = Gtk.Label("destination_address:")
        self.udp_destination_address_entry = Gtk.Entry()
        self.udp_destination_address_entry.set_text("0")  # 默认为0

        udp_send_button = Gtk.Button(label="Send")
        udp_send_button.connect("clicked", self.udp_sender)

        # 添加UDP标签页到Notebook
        notebook.append_page(udp_tab, Gtk.Label("UDP"))


        udp_tab.attach(udp_source_port_label, 0, 0, 1, 1)
        udp_tab.attach(self.udp_source_port_entry, 1, 0, 1, 1)

        udp_tab.attach(udp_destination_port_label, 2, 0, 1, 1)
        udp_tab.attach(self.udp_destination_port_entry, 3, 0, 1, 1)

        udp_tab.attach(udp_data_label, 0, 1, 1, 1)
        udp_tab.attach(self.udp_data_entry, 1, 1, 1, 1)

        udp_tab.attach(udp_source_address_label, 0, 2, 1, 1)
        udp_tab.attach(self.udp_source_address_entry, 1, 2, 1, 1)

        udp_tab.attach(udp_destination_address_label, 2, 2, 1, 1)
        udp_tab.attach(self.udp_destination_address_entry, 3, 2, 1, 1)

        udp_tab.attach(udp_send_button, 4, 3, 1, 1)

        # 创建ICMP标签页
        icmp_tab = Gtk.Grid()
        icmp_tab.set_border_width(3)

        # ICMP 参数文本框
        icmp_type_label = Gtk.Label("type:")
        self.icmp_type_entry = Gtk.Entry()
        self.icmp_type_entry.set_placeholder_text("请输入request或reply")

        icmp_identification_label = Gtk.Label("identification:")
        self.icmp_identification_entry = Gtk.Entry()
        self.icmp_identification_entry.set_text("1")  # 默认为

        icmp_code_label = Gtk.Label("code:")
        self.icmp_code_entry = Gtk.Entry()
        self.icmp_code_entry.set_text("1")  # 默认为

        icmp_destination_address_label = Gtk.Label("destination address:")
        self.icmp_destination_address_entry = Gtk.Entry()
        self.icmp_destination_address_entry.set_text("0")  # 默认为0

        icmp_sequence_label = Gtk.Label("sequence:")
        self.icmp_sequence_entry = Gtk.Entry()
        self.icmp_sequence_entry.set_text("0")  # 默认为0

        icmp_send_button = Gtk.Button(label="Send")
        icmp_send_button.connect("clicked", self.icmp_sender)

        # 添加ICMP标签页到Notebook
        notebook.append_page(icmp_tab, Gtk.Label("ICMP"))

        icmp_tab.attach(icmp_type_label, 0, 0, 1, 1)
        icmp_tab.attach(self.icmp_type_entry, 1, 0, 1, 1)

        icmp_tab.attach(icmp_identification_label, 2, 0, 1, 1)
        icmp_tab.attach(self.icmp_identification_entry, 3, 0, 1, 1)

        icmp_tab.attach(icmp_code_label, 4, 0, 1, 1)
        icmp_tab.attach(self.icmp_code_entry, 5, 0, 1, 1)

        icmp_tab.attach(icmp_destination_address_label, 0, 1, 1, 1)
        icmp_tab.attach(self.icmp_destination_address_entry, 1, 1, 1, 1)

        icmp_tab.attach(icmp_sequence_label, 2, 1, 1, 1)
        icmp_tab.attach(self.icmp_sequence_entry, 3, 1, 1, 1)

        icmp_tab.attach(icmp_send_button, 3, 2, 1, 1)



        # 创建ARP标签页
        arp_tab = Gtk.Grid()
        arp_tab.set_border_width(3)
        # ARP 参数文本框
        operation_code_label = Gtk.Label("operation_code:")
        self.operation_code_entry = Gtk.Entry()
        self.operation_code_entry.set_placeholder_text("请输入request或reply")

        interface_label = Gtk.Label("interface:")
        self.interface_entry = Gtk.Entry()
        self.interface_entry.set_text(os.listdir('/sys/class/net/')[0])  # 默认为0

        source_hardware_address_label = Gtk.Label("source_hardware_address:")
        self.source_hardware_address_entry = Gtk.Entry()
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.source_hardware_address_entry.set_text(":".join([mac[e:e + 2] for e in range(0, 11, 2)]))  # 默认为0

        source_protocol_address_label = Gtk.Label("source_protocol_address:")
        self.source_protocol_address_entry = Gtk.Entry()
        self.source_protocol_address_entry.set_text(ip)  # 默认为0

        destination_hardware_address_label = Gtk.Label("destination_hardware_address:")
        self.destination_hardware_address_entry = Gtk.Entry()
        self.destination_hardware_address_entry.set_text("00:00:00:00:00:00")  # 默认为0

        destination_protocol_address_label = Gtk.Label("destination_protocol_address:")
        self.destination_protocol_address_entry = Gtk.Entry()
        self.destination_protocol_address_entry.set_text("0")  # 默认为0

        arp_send_button = Gtk.Button(label="Send")
        arp_send_button.connect("clicked", self.arp_sender)

        # 添加ARP标签页到Notebook
        notebook.append_page(arp_tab, Gtk.Label("ARP"))

        arp_tab.attach(operation_code_label, 0, 0, 1, 1)
        arp_tab.attach(self.operation_code_entry, 1, 0, 1, 1)

        arp_tab.attach(interface_label, 2, 0, 1, 1)
        arp_tab.attach(self.interface_entry, 3, 0, 1, 1)

        arp_tab.attach(source_hardware_address_label, 0, 1, 1, 1)
        arp_tab.attach(self.source_hardware_address_entry, 1, 1, 1, 1)

        arp_tab.attach(source_protocol_address_label, 2, 1, 1, 1)
        arp_tab.attach(self.source_protocol_address_entry, 3, 1, 1, 1)

        arp_tab.attach(destination_hardware_address_label, 0, 2, 1, 1)
        arp_tab.attach(self.destination_hardware_address_entry, 1, 2, 1, 1)

        arp_tab.attach(destination_protocol_address_label, 2, 2, 1, 1)
        arp_tab.attach(self.destination_protocol_address_entry, 3, 2, 1, 1)

        arp_tab.attach(arp_send_button, 3, 3, 1, 1)


    # 获取用户输入的信息，构造IP报文并发送和添加记录
    def ip_sender(self, button):
        ip_pack = {}
        ptcl = {'TCP': 6, 'UDP': 17, 'ICMP': 1}

        ip_pack["ds"] = int(self.ds_entry.get_text())

        ip_pack['identification'] = int(self.ip_identification_entry.get_text())

        ip_pack['flag'] = int(self.df_entry.get_text()) * 2 + int(self.mf_entry.get_text())

        ip_pack['frag_off'] = int(self.ip_frag_off_entry.get_text())

        ip_pack['time_to_live'] = int(self.time_to_live_entry.get_text())

        ip_pack['protocol'] = ptcl[self.ip_protocol_entry.get_text()]

        ip_pack['source_address'] = self.ip_source_address_entry.get_text()

        ip_pack['destination_address'] = self.ip_destination_address_entry.get_text()

        ip_pack['option'] = self.ip_option_entry.get_text()

        ip_pack['data'] = self.ip_data_entry.get_text()

        ip_packet = IP_Packet(ip_pack)
        ip_packet.send(int(self.ip_destination_port_entry.get_text()))

    # 获取用户输入的信息，构造TCP报文并发送和添加记录
    def tcp_sender(self, button):

        tcp_pack = {}

        tcp_pack['source_port'] = int(self.tcp_source_port_entry.get_text())

        tcp_pack['destination_port'] = int(self.tcp_destination_port_entry.get_text())

        tcp_pack['sequence'] = int(self.tcp_sequence_entry.get_text())

        tcp_pack['acknowledge_num'] = int(self.acknowledge_num_entry.get_text())

        tcp_pack['URG'] = int(self.URG_entry.get_text())

        tcp_pack['ACK'] = int(self.ACK_entry.get_text())  # TCP 规定，在连接建立后所有传送的报文段都必须把 ACK 设置为 1

        tcp_pack['PSH'] = int(self.PSH_entry.get_text())

        tcp_pack['RST'] = int(self.RST_entry.get_text())

        tcp_pack['SYN'] = int(self.SYN_entry.get_text())

        tcp_pack['FIN'] = int(self.FIN_entry.get_text())

        tcp_pack['window'] = int(self.window_entry.get_text())

        tcp_pack['urg_point'] = int(self.urg_point_entry.get_text())

        tcp_pack['option'] = self.tcp_option_entry.get_text()

        tcp_pack['data'] = self.tcp_data_entry.get_text()

        tcp_pack['source_address'] = self.tcp_source_address_entry.get_text()

        tcp_pack['destination_address'] = self.tcp_destination_address_entry.get_text()

        tcp_packet = TCP_Packet(tcp_pack)
        tcp_packet.send()


# 获取用户输入的信息，构造UDP报文并发送和添加记录
    def udp_sender(self, button):
        udp_pack = {}

        udp_pack['source_address'] = self.udp_source_address_entry.get_text()

        udp_pack['destination_address'] = self.udp_destination_address_entry.get_text()

        udp_pack['source_port'] = int(self.udp_source_port_entry.get_text())

        udp_pack['destination_port'] = int(self.udp_destination_port_entry.get_text())

        udp_pack['data'] = self.udp_data_entry.get_text()

        udp_packet = UDP_Packet(udp_pack)
        udp_packet.send()


# 获取用户输入的信息，构造ARP报文并发送和添加记录
    def arp_sender(self, button):
        op_dict = {'request': OP_REQUEST, 'reply': OP_REPLY}
        arp_pack = {}

        arp_pack["operation_code"] = op_dict[self.operation_code_entry.get_text()]

        arp_pack["interface"] = self.interface_entry.get_text()

        arp_pack["source_hardware_address"] = self.source_hardware_address_entry.get_text()

        arp_pack["source_protocol_address"] = self.source_protocol_address_entry.get_text()

        arp_pack["destination_hardware_address"] = self.destination_hardware_address_entry.get_text()

        arp_pack["destination_protocol_address"] = self.destination_protocol_address_entry.get_text()

        arp_packet = ARP_Packet(arp_pack)
        arp_packet.send(arp_pack["interface"])


# 获取用户输入的信息，构造ICMP报文并发送和添加记录
    def icmp_sender(self, button):
        type_dict = {'request': 8, 'reply': 0}
        icmp_pack = {}

        icmp_pack["type"] = type_dict[self.icmp_type_entry.get_text()]  # 0:ping应答；8:ping请求

        icmp_pack["code"] = int(self.icmp_code_entry.get_text())

        icmp_pack["identification"] = int(self.icmp_identification_entry.get_text())

        icmp_pack["sequence"] = int(self.icmp_sequence_entry.get_text())

        icmp_pack["destination_address"] = self.icmp_destination_address_entry.get_text()

        icmp_packet = ICMP_Packet(icmp_pack)
        icmp_packet.send(icmp_pack["destination_address"])


if __name__ == '__main__':
    win = NetworkConfigWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

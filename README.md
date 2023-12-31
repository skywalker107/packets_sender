# Packets_Sender

## 一、项目介绍

#### 1.项目内容简述：

该项目利用Python语言，构建较为完整的IP报文、TCP报文、UDP报文、ICMP报文和ARP报文并实现发送到网络上。

#### 2.平台和语言：

项目基于Linux平台，使用Python语言，借助socket、os、PyGTK等库进行编写。

#### 3.项目使用：

在Linux系统中打开终端，使用命令

```
git clone https://github.com/skywalker107/packets_sender.git
cd packets_sender
sudo python3 main.py
```

若没有安装PyGTK，可以使用命令

```
pip install PyGObject
```

进行安装。

## 二、项目结构与功能

#### 1.报文种类与字段构造

每个报文构成一个类，每个报文类的具有相似的结构和不同的细节。每个报文类都会接受来自主函数的列表内容，来进行对应报文类的字段初始化和赋值。

##### （1）IP报文类（IP.py）

###### ①字段：

IP版本（version）、首部长度（header_len）、区分服务（ds）、标识（identification）、标志（flag）、片偏移（frag_off）、生存时间（ttl）、协议（protocol）、头部校验和（header_check_sum）、源IP地址（source_address）、目的IP地址（destination_address）、可选项（option）、数据（data）、总长度（total_len）

###### ②函数：

计算头部校验和（check_sum_cal）

打包全部内容（pack）

发送包内容（send）

##### （2）TCP报文类（TCP.py）

###### ①字段：

源端口（source_port）、目的端口（destination_port）、源IP地址（source_address）、目的IP地址（destination_address）、序列号（sequence）、确认号（acknowledge_num）、偏移（data_offset）、保留内容（reserved）、URG、ACK、PSH、RST、FIN、窗口（window）、校验和（check_sum）、紧急指针（urg_point)、可选项（option)、数据（data)

###### ②函数：

计算头部校验和（check_sum_cal）

打包全部内容（pack）

发送包内容（send）

##### （3）UDP报文类（UDP.py）

###### ①字段：

源端口（source_port）、目的端口（destination_port）、总长度（length）、校验和（check_sum）、数据（data）、源IP地址（source_address）、目的IP地址（destination_address）

###### ②函数：

计算头部校验和（check_sum_cal）

打包全部内容（pack）

发送包内容（send）

##### （4）ICMP报文类（ICMP.py）

###### ①字段：

ICMP类型（type）、代码（code）、校验和（check_sum）、标识（identification）、序列号（sequence）

###### ②函数：

计算头部校验和（check_sum_cal）

打包全部内容（pack）

发送包内容（send）

##### （5）ARP报文类（ARP.py）

###### ①字段：

硬件类型（hardware_type）、协议类型（protocol_type）、MAC地址长度（hardware_length）、IP地址长度（protocol_length）、操作代码（operation_code）、源MAC地址（source_hardware_address）、目的MAC地址（destination_hardware_address）、源IP地址（source_address）、目的IP地址（destination_address）、广播地址（broadcast）

###### ②函数：

计算头部校验和（check_sum_cal）

打包全部内容（pack）

发送包内容（send）

#### 2.主要函数与界面设计（main.py）

##### （1）主要函数

用于接受PyGTK文本框输入内容并赋值给相应列表项，然后将列表赋值给相应报文类进行初始化并发送。

包括：

ip_sender(self, button)、tcp_sender(self, button)、udp_sender(self, button)、arp_sender(self, button)、icmp_sender(self, button)

##### (2)界面设计

采用PyGTK进行设计，运行后效果图：

###### IP界面

![IP](.\screen_shot\IP.png)

对应的字段内容需要根据特定的灰色文字提示进行输入，输入完成后点击发送即可发送到对应的地址。

以下是其他四种报文界面的效果图：

###### TCP界面

![TCP](.\screen_shot\TCP.png)

###### UDP界面

![UDP](.\screen_shot\UDP.png)

###### ICMP界面

![ICMP](.\screen_shot\ICMP.png)

###### ARP界面

![ARP](.\screen_shot\ARP.png)

每个报文中的标签和输入文本框采用Gtk.grid()进行网格化，以便于界面的美化和分配。

# 三、暂未实现和未来工作

1.错误处理

对于错误输入的内容和形式（如需要输入16进制但输入了10进制内容），未实现错误提示，未来会实现对错误提示的工作，通过多种细节处理和判断，提示不同的错误信息。

2.完善报文种类

报文种类未完全完善，如ICMP报文还包括超时、改变路由、参数问题等多种报文类型，此处只实现了请求和响应报文，将在未来对多种报文类型的完善方面做出工作。

3.更加完善界面

目前界面形式已初步确定，同时可以进行缩放，但界面分配和界面留白等仍存在，未来可以对界面的美观程度进行增强。
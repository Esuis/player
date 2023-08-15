# -*- coding: utf-8 -*-

import binascii
from scapy.all import sniff
from scapy.layers.inet import TCP
from scapy.layers.inet6 import IPv6
import scapy


flow_info = {}

# 定义回调函数来处理捕获的数据包
def packet_callback(packet):
    if IPv6 in packet and packet.haslayer("IPv6ExtHdrHopByHop"):
        # 获取HBH信息
        hbh_header = packet["IPv6ExtHdrHopByHop"]
        options = hbh_header.options
       
        # 查找自定义的HBH选项
        for option in options:
            if option.otype == 0x3c:
                # print("Scapy6 Unknown Option:")
                # print("otype: {}".format(option.otype))
                # print("optlen: {}".format(option.optlen))
                # print("optdata: {}".format(binascii.hexlify(option.optdata)))
                num = int(binascii.hexlify(option.optdata),16)
                # print("optdata:{}".format(bin(num)[2:]))
                
                #获取到的二进制APN信息
                QoE_usr       = num >> 93       #用户类型
                QoE_sex       = (num >> 92) & 0b1       #性别
                QoE_edu       = (num >> 88) & 0b1111      #教育程度
                QoE_major     = (num >> 84) & 0b1111     #专业
                QoE_age       = (num >> 80) & 0b1111       #年龄
                QoE_app       = (num >> 76) & 0b1111       #应用类型
                QoE_qoe_i     = (num >> 72) & 0b1111     #QoE得分整数部分
                QoE_loss      = (num >> 64) & 0b11111111      #丢包率
                QoE_delay     = (num >> 48) & 0b1111111111111111     #时延
                QoE_qoe_f     = (num >> 32) & 0b1111111111111111           #QoE得分小数部分
                QoE_bandwidth = num & 0b11111111111111111111111111111111  #带宽

                #打印二进制APN信息
                # print("QoE_usr: {}".format(bin(QoE_usr)[2:]))
                # print("QoE_sex: {}".format(bin(QoE_sex)[2:]))
                # print("QoE_edu: {}".format(bin(QoE_edu)[2:]))
                # print("QoE_major: {}".format(bin(QoE_major)[2:]))
                # print("QoE_age: {}".format(bin(QoE_age)[2:]))
                # print("QoE_app: {}".format(bin(QoE_app)[2:]))
                # print("QoE_qoe_i: {}".format(bin(QoE_qoe_i)[2:]))
                # print("QoE_bandwith: {}".format(bin(QoE_bandwidth)[2:]))
                # print("QoE_delay: {}".format(bin(QoE_delay)[2:]))
                # print("QoE_loss: {}".format(bin(QoE_loss)[2:]))
                # print("QoE_qoe_f: {}".format(bin(QoE_qoe_f)[2:]))
                # print("--------------------------------")

                #处理QoE得分的函数
                def handle_qoe(qoe_i, qoe_f):
                    qoe_i = int(bin(QoE_qoe_i), 2)

                    qoe_f = int(bin(QoE_qoe_f), 2)
                    qoe_f = float(qoe_f)
                    if qoe_f < 10:
                       qoe_f = qoe_f / 10
                    elif 10 <= qoe_f < 100:
                        qoe_f = qoe_f / 100
                    elif 100 <= qoe_f < 1000:
                        qoe_f = qoe_f / 1000
                    elif 1000 <= qoe_f < 10000:
                        qoe_f = qoe_f / 10000
                    elif 10000 <= qoe_f < 100000:
                        qoe_f = qoe_f / 100000
                    
                    qoe = qoe_i + qoe_f
                    return qoe  
                
                #处理网络参数的函数
                def handle_net(net):
                    value = net & 0b00001111
                    #print(value)
                    unit = net >> 4
                    #print(unit)
                    net = int(bin(value),2)
                    if unit == 0b0000:
                        net = net
                    elif unit == 0b0001:
                        net = net * 10
                    elif unit == 0b0010:
                        net = net * 100
                    elif unit == 0b0100:
                        net = net * 1000
                    elif unit == 0b1000:
                        net = net * 10000
                    return net
                    

                #将二进制APN信息转为十进制
                usr         = int(bin(QoE_usr), 2)
                sex         = int(bin(QoE_sex), 2)
                edu         = int(bin(QoE_edu), 2)
                major       = int(bin(QoE_major), 2)
                age         = int(bin(QoE_age), 2)
                app         = int(bin(QoE_app), 2)
                bandwidth   = int(bin(QoE_bandwidth), 2)
                delay       = int(bin(QoE_delay), 2)
                loss        = handle_net(QoE_loss)
                qoe         = handle_qoe(QoE_qoe_i, QoE_qoe_f)

                print("用户类型: {}".format(usr))
                print("性别: {}".format(sex))
                print("受教育程度: {}".format(edu))
                print("专业: {}".format(major))
                print("年龄: {}".format(age))
                print("应用类型: {}".format(app))
                print("带宽: {}".format(bandwidth))
                print("时延: {}".format(delay))
                print("丢包率: {}".format(loss))
                print("qoe分数: {}".format(qoe))
                print("--------------------------------")


                #打印IPv6的地址和TCP端口
                src_ipv6 = packet[IPv6].src
                dst_ipv6 = packet[IPv6].dst
                # print("Packet:")
                # print("Source IPv6:", src_ipv6)
                # print("Destination IPv6:", dst_ipv6)
                # if packet.haslayer(TCP):
                #     print("TCP Source Port:", packet[TCP].sport)
                #     print("TCP Destination Port", packet[TCP].dport)
                # print("--------------------------------")

                                
                #数据包头中的apn信息存储在字典中
                apn_info = {
                    "src_ipv6":src_ipv6,
                    "dst_ipv6":dst_ipv6,
                    "usr":usr,
                    "sex":sex,
                    "edu":edu,
                    "major":major,
                    "age":age,
                    "app":app,
                    "bandwidth":bandwidth,
                    "delay":delay,
                    "loss":loss,
                    "qoe":qoe
                }

                session = (src_ipv6, dst_ipv6)
                if session not in flow_info:
                    flow_info[session] = []
                    flow_info[session].append(apn_info)
                

                # if qoe < 3:

                #     command = "ovs-vsctl set queue"
                #     uuid = "eeb42583-7e72-4cd1-8f69-5a9dc4afea94"
                #     other_config = "other-config:min-rate=600000 other-config:max-rate=1000000"
                #     send_queue_command(command, uuid, other_config)

                #     command = "ovs-ofctl add-flow"
                #     bridge = "s2"
                #     other_config = "ipv6,ipv6_dst=2001:250:1001:1044::33,in_port=s2-eth3,actions=set_queue:2,output=eno2"
                #     send_flow_command(command,bridge,other_config)


                # print("--------------------------------")


pcap_name = "capture_302.pcap"
packets = scapy.utils.rdpcap(pcap_name)
packet_callback(packets[1])
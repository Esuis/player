# -*- coding: utf-8 -*-

import binascii
from scapy.all import sniff
from scapy.layers.inet import TCP
from scapy.layers.inet6 import IPv6
import scapy




# 定义回调函数来处理捕获的数据包
def process_packet(packet):
    if IPv6 in packet and packet.haslayer("IPv6ExtHdrHopByHop"):
        # 获取HBH信息
        hbh_header = packet["IPv6ExtHdrHopByHop"]
        options = hbh_header.options
       
        # 查找自定义的HBH选项
        for option in options:
            if option.otype == 0x3c:
                print("Scapy6 Unknown Option:")
                print("otype: {}".format(option.otype))
                print("optlen: {}".format(option.optlen))
                print("optdata: {}".format(binascii.hexlify(option.optdata)))
                num = int(binascii.hexlify(option.optdata),16)
                print("optdata:{}".format(bin(num)[2:]))

                #掩码，用于按位获取信息
                mask_usr       = 0b1110000000000000000000000000000000000000000000000000000000000000
                mask_sex       = 0b0001000000000000000000000000000000000000000000000000000000000000
                mask_edu       = 0b0000111100000000000000000000000000000000000000000000000000000000
                mask_major     = 0b0000000011110000000000000000000000000000000000000000000000000000
                mask_age       = 0b0000000000001111000000000000000000000000000000000000000000000000
                mask_app       = 0b0000000000000000111100000000000000000000000000000000000000000000
                mask_qoe_i     = 0b0000000000000000000011110000000000000000000000000000000000000000
                mask_bandwidth = 0b0000000000000000000000001111111100000000000000000000000000000000
                mask_delay     = 0b0000000000000000000000000000000011111111000000000000000000000000
                mask_loss      = 0b0000000000000000000000000000000000000000111111110000000000000000
                mask_qoe_f     = 0b0000000000000000000000000000000000000000000000001111111111111111
                
                #获取到的二进制APN信息
                QoE_usr       = (num & mask_usr) >> 61       #用户类型
                QoE_sex       = (num & mask_sex) >> 60       #性别
                QoE_edu       = (num & mask_edu) >> 56       #教育程度
                QoE_major     = (num & mask_major) >> 52     #专业
                QoE_age       = (num & mask_age) >> 48       #年龄
                QoE_app       = (num & mask_app) >> 44       #应用类型
                QoE_qoe_i     = (num & mask_qoe_i) >> 40     #QoE得分整数部分
                QoE_bandwidth = (num & mask_bandwidth) >> 32  #带宽
                QoE_delay     = (num & mask_delay) >> 24     #时延
                QoE_loss      = (num & mask_loss) >> 16      #丢包率
                QoE_qoe_f     = (num & mask_qoe_f)           #QoE得分小数部分


                #打印二进制APN信息
                print("QoE_usr: {}".format(bin(QoE_usr)[2:]))
                print("QoE_sex: {}".format(bin(QoE_sex)[2:]))
                print("QoE_edu: {}".format(bin(QoE_edu)[2:]))
                print("QoE_major: {}".format(bin(QoE_major)[2:]))
                print("QoE_age: {}".format(bin(QoE_age)[2:]))
                print("QoE_app: {}".format(bin(QoE_app)[2:]))
                print("QoE_qoe_i: {}".format(bin(QoE_qoe_i)[2:]))
                print("QoE_bandwith: {}".format(bin(QoE_bandwidth)[2:]))
                print("QoE_delay: {}".format(bin(QoE_delay)[2:]))
                print("QoE_loss: {}".format(bin(QoE_loss)[2:]))
                print("QoE_qoe_f: {}".format(bin(QoE_qoe_f)[2:]))

                print("--------------------------------")

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
                bandwidth   = handle_net(QoE_bandwidth)
                delay       = handle_net(QoE_delay)
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


                #打印IPv6的地址和TCP端口
                if packet.haslayer(IPv6):
                    print("Packet:")
                    print("Source IPv6:", packet[IPv6].src)
                    print("Destination IPv6:", packet[IPv6].dst)

                    if packet.haslayer(TCP):
                        print("TCP Source Port:", packet[TCP].sport)
                        print("TCP Destination Port", packet[TCP].dport)

                print("--------------------------------")


pcap_name = "capture_8.pcap"
packets = scapy.utils.rdpcap(pcap_name)
process_packet(packets[1])
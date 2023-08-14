"""
读取pcap包
FenLiu区分会话(使用过的端口)
FenBao按照会话形成二维数组，第一维是使用过的端口列表，里面存储这个端口下的会话pcap
GetLossrate计算丢包率
"""

import matplotlib.pyplot as plt
import scapy
from scapy.all import sniff
from scapy.layers.inet import Ether, TCP
from scapy.layers.inet6 import IPv6
import os
import threading


pcap = './pcap/test4.pcap'
parm = [1.26, 4.3, 1.1, 0.8, 0.6, 0.05, 0.35, 0.2]  # miu, omega, niu, eta, alpha, beta, gamma, lambda
netpcapnum = 2000

write_event = threading.Event()

class ScapyPcap:
    def __init__(self, pcap_name):
        print('开始读取pcap')
        print('pcap包名称为:', pcap_name)
        while True:
            try:
                write_event.wait()
                print(write_event.is_set())
                # file_path = '/path/to/file.txt'
                if os.path.isfile(pcap_name):
                    file_size = os.path.getsize(pcap_name)
                    print(f"文件大小为: {file_size} 字节")
                    # if file_size < 30:
                    #     print(write_event.is_set())
                    #     print("文件写入未完成")
                    #     continue
                    # else:
                    #     print(f"文件大小为: {file_size} 字节")
                else:
                    print("文件不存在")
                    
                
                self.packets = scapy.utils.rdpcap(pcap_name)
                self.pktslen = len(self.packets)
                self.name = pcap_name
                print('读取完成')
                write_event.clear()
                break
            except:
                print('数据包不可读')
                continue

        # 公式中的各个参数
        self.miu = parm[0]
        self.omiga = parm[1]
        self.niu = parm[2]
        self.eta = parm[3]
        self.alpha = parm[4]
        self.beta = parm[5]
        self.gamma = parm[6]
        self.lamda = parm[7]
        self.playout_bitrate = 2000
        self.frame_rate = 25
        self.height = 720
        self.rebuffer_duration_sec = 0
        self.rebuffer_number = 0
        self.fei = 1
        self.Bu = 1  # 视频带宽

    """
    # TODO 还没有分IP，以下都应该在分好IP的情况下进行
    """
    def FenLiu(self):  # 按照五元组区分会话，同时去除掉服务器一直使用的80端口
        # set用于去重
        set_port = set()
        l = len(self.packets)
        
        for i in range(0, l):
            try:
                # 添加所有TCP数据包的端口
                if self.packets[i]['TCP'].sport:
                    set_port.add(self.packets[i]['TCP'].sport)
            except:
                pass
        set_port.discard(80)
        print("各会话中客户端所使用过的端口号为：", set_port)
        return set_port

    def FenBao(self):  # 形成一个二维数组，第一维是使用过的端口列表，里面存储这个端口下的会话pcap
        set_port = list(self.FenLiu())
        l1 = len(set_port)
        data_list = [[] for _ in range(l1)]  # 长度为除了80端口外所有使用过的端口个数
        l = len(self.packets)  # 总包数
        for i in range(0, l):
            try:
                # 源端口在port列表里，则端口获取在列表中的索引，放入对应的data_list中
                if self.packets[i]['TCP'].sport in set_port:
                    j = set_port.index(self.packets[i]['TCP'].sport)
                    data_list[j].append(self.packets[i])
                # 目的端口在port列表里，则端口获取在列表中的索引，放入对应的data_list中
                elif self.packets[i]['TCP'].dport in set_port:
                    j = set_port.index(self.packets[i]['TCP'].dport)
                    data_list[j].append(self.packets[i])
            except:
                pass

        return data_list

    def GetLossrate(self):  # 从接收端的ack获取丢包率，当ack重复出现时说明发生丢包
        set_port = list(self.FenLiu())
        data_list = self.FenBao()
        total = 0
        total_loss = 0
        for i in range(0, len(data_list)):
            loss = -2  # 去除握手中SYN及FIN的ACK重复
            pktnum = 0
            ack_list = set()  # 用于存放所有ack
            print("*************************************")
            print("当前会话客户端使用的端口号为：", set_port[i])
            for pkt in data_list[i]:
                ack = pkt[TCP].ack
                if ack in ack_list and ack != 1:
                    if pkt[IPv6].src == "2001:250:1001:1044::c1":  # 只考虑客户端的ack
                        pktnum -= 1  # 只考虑客户端发包情况时，滤除服务器发包被抓到的包
                        pass
                    else:
                        loss += 1
                        # print(ack)
                else:
                    ack_list.add(ack)
                pktnum += 1
            loss = loss if loss > -1 else 0
            print("本会话共", pktnum, "包，丢失", loss, "包")
            total += pktnum
            total_loss += loss if loss > -1 else 0
        lossrate = (total_loss / total * 100) if total != 0 else -1
        print("-------------------------------------")
        print("-------------------------------------")
        print('pcap包名称为:', self.name)
        print("共计", total, "包，丢失", total_loss, "包，丢包率", '%.2f'%lossrate, "%")
        print("-------------------------------------")
        print("-------------------------------------")
        return lossrate

    def GetByteVel(self):
        j = 0  # 计数器
        timedif = []
        tmp_time = 0
        pktnum = 200  # 每200包计算一次包到达速率
        pktvel = 0
        for pkt in self.packets:
            if pkt[IPv6].dst == "2001:250:1001:1044::c1":  # 只考虑客户端收包情况
                if j == pktnum:
                    last_time = pkt[TCP].time
                    pktvel = (last_time - tmp_time) / pktnum
                '''
                last_time = 0 if tmp_time == 0 else tmp_time
                tmp_time = pkt['TCP'].time
                time_dif = tmp_time - last_time
                timedif.append(time_dif)
                '''
                j += 1
                if tmp_time == 0:
                    tmp_time = pkt['TCP'].time
            else:
                pass
            print('每', pktnum, '包计算一次包到达速率，其结果为', pktvel)

    def GetLossrate_AsNo(self):  # 根据包个数进行计算丢包率
        j = 0  # 计数器
        loss = 0
        loss_list = []
        ack_list = set()
        for pkt in self.packets:
            ack = pkt[TCP].ack
            if ack in ack_list and ack != 1:
                if pkt[IPv6].dst == "2001:250:1001:1044::c1":  # 只考虑客户端的ack
                    # j -= 1
                    pass
                else:
                    loss += 1
            else:
                ack_list.add(ack)
            j += 1
            if j == 200:  # 每200包统计一次
                loss = loss if loss > -1 else 0
                lossrate = loss / j * 100
                print('当前统计', j, '包，丢失', loss, '包，丢包率', '%.2f'%lossrate, "%")
                loss_list.append(lossrate)
                j = 0
                loss = 0
        plt.plot(loss_list)
        plt.show()

    def getDly(self, ack3pkt, seqpkt):  # 计算延迟
        """
        延迟的计算方法：当发生TCP快速重传时，服务器会直接重传相应的seq分片，则延迟时间为两段时间差/2
        :param ack3pkt:
        :param seqpkt:
        :return:
        """
        lastack_time = ack3pkt.time
        fastreseq_time = seqpkt.time
        delay = (fastreseq_time - lastack_time) / 2
        return delay


def Callback(packet):  # 下面inlineget函数的参数
    print('src:%s----->dst:%s'%(packet[IPv6].src, packet[IPv6].dst))
    print('TTL:%s'%packet[IPv6].ttl)

def onlineget():  # 使用sniff在线抓包并保存为pcap
    # TODO 这里是用IP区分当前视频服务的包和其他包，在真实场景中，该如何获取本机ip或视频服务器对应的ip需进一步改进
    print('开始捕获网络包2')
    host = "2001:250:1001:1044::9d"
    filter_str = f"ip6 host {host}"
    packet = sniff(filter=filter_str, iface = "eno1", prn = lambda x: x.summary(), count = netpcapnum)
    print('网络包捕获完成2')
    scapy.utils.wrpcap('data_ori.pcap', packet)

def filter_packets(input_file, output_file, filter_ip):
    packets  = scapy.utils.rdpcap(input_file)
    # 这里过滤的是dst.ip
    filtered_packets = [pkt for pkt in packets if IPv6 in pkt and pkt[IPv6].dst == filter_ip]
    scapy.utils.wrpcap(output_file, filtered_packets)


def GetDelay(pcapname, dst_ip):

    packets = scapy.utils.rdpcap(pcapname)
    print("GetDelay_pcapname: ",pcapname)

    # 字典用于存储数据包的时间戳
    timestamps = {}
    first_pkt = 1
    ack_num = 0

    for packet in packets:
        # 
        if packet.haslayer(IPv6) and packet[IPv6].dst == dst_ip and packet.haslayer(TCP):  # dst_ip为server地址
            
            timestamp = packet.time
            ack_num = packet[TCP].ack
            timestamps[ack_num] = timestamp
            if first_pkt == 1:
                first_ack = ack_num
                first_pkt = 0

    # 根据时间戳计算延迟
    total_packets = len(packets)
    print("delay_packets: ",total_packets)
    # print("timestamps[first_ack]: ",timestamps[first_ack])
    # print("timestamps[ack_num]: ",timestamps[ack_num])
    delaytime = -1
    if ack_num and total_packets > 1 :
        delaytime = abs(timestamps[ack_num]-timestamps[first_ack]) / (2 * ( total_packets - 1 ))
    # print(delaytime)
    # print(delaytime*1000)
    delaytime = float(delaytime)
    # print(delaytime)
    
    
    # delays = []
    # for packet in packets:
    #     # 
    #     if packet.haslayer(IPv6) and packet[IPv6].src == dst_ip:
    #         timestamp = packet.time
    #         seq_num = packet[TCP].seq
    #         # 检查该序列号是否存在于字典中
    #         if seq_num in timestamps:
    #             # 计算延迟
    #             delay = timestamps[seq_num] - timestamp
    #             delays.append(delay)

    # 各个延迟
    # for i, delay in enumerate(delays):
    #     print("Delay {}: {:.6f} seconds".format(i + 1, delay))

    # 平均延迟
    # if len(delays) > 0:
    #     avg_delay = sum(delays) / len(delays)
    #     print("本段连接中共捕获", len(delays), "段 seq 与 ack 应答，其平均延迟为：", avg_delay)
    #     return avg_delay
    # else:
        # print("未捕获到延迟值")
        # return None

    if delaytime >= 0:

        return delaytime
    else:
        print("未捕获到延迟值")
        
        return delaytime






if __name__ == '__main__':
    # 计算离线pcap丢包率及qoe分数
    # SiyuanPcap2 = ScapyPcap(pcap)
    # # total_lossrate = SiyuanPcap2.GetLossrate()
    # # SiyuanPcap2.GetLossrate_AsNo()
    # SiyuanPcap2.GetByteVel()
    # QoE = SiyuanPcap2.QoEScore()

    # 计算在线抓包信息
    onlineget()
    filter_packets('data_ori.pcap', 'data.pcap', '2001:250:1001:1044::9d')
    WangluoPcap = ScapyPcap('data.pcap')
    WangluoPcap.GetLossrate()
    GetDelay('data_ori.pcap', '2001:250:1001:1044::c1')


from scapy.all import *
from scapy.layers.inet6 import IPv6
from scapy.layers.inet import TCP

def sniff_and_save_ipv6_packets(host, filename):
    # 定义IPv6主机过滤器
    filter_str = f"ip6 host {host}"

    # 开始捕获并保存数据包到文件
    packets = sniff(filter=filter_str, iface="eno1", count=2000)
    wrpcap(filename, packets)

    # 打印捕获的数据包数量
    print(f"捕获到的满足IPv6主机过滤器 {host} 的数据包数量: {len(packets)}")

# 指定目标IPv6主机和保存文件名
# 指定目标IPv6主机和网络接口进行捕获
host = "2001:250:1001:1044::9d"
filename = "captured_packets.pcap"

# 调用函数进行数据包捕获和保存
sniff_and_save_ipv6_packets(host, filename)

packets = scapy.utils.rdpcap(filename)

# 字典用于存储数据包的时间戳
timestamps = {}
dst_ip = "2001:250:1001:1044::9d"
for packet in packets:
    # 检查数据包是否是从服务器发送到客户端的
    print(packet[IPv6].dst == dst_ip)
    if packet.haslayer(IPv6) and packet[IPv6].dst == dst_ip:  # dst_ip为客户端地址
        timestamp = packet.time
        seq_num = packet[TCP].seq
        timestamps[seq_num] = timestamp
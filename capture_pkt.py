import threading
import queue
from scapy.layers.inet import Ether, TCP
from scapy.layers.inet6 import IPv6
from scapy.all import sniff
import scapy

write_event = threading.Event()

capture_duration = 2  # 捕获持续时间（秒）
capture_flag = True  # 捕获标志
pcap_counter = 0  # pcap文件计数器
pcap_queue = queue.Queue()
filter_ip = "2001:250:1001:1044::9d"

def capture_pkt():
    global pcap_counter
    while capture_flag:
        # TODO 这里是用IP区分当前视频服务的包和其他包，在真实场景中，该如何获取本机ip或视频服务器对应的ip需进一步改进
        print('开始捕获网络包')
        host = "2001:250:1001:1044::9d"
        filter_str = f"ip6 host {host}"
        packet = sniff(filter=filter_str, timeout=capture_duration)
        print('网络包捕获完成')
        filtered_packets = [pkt for pkt in packet if IPv6 in pkt and pkt[IPv6].dst == filter_ip]
        pcap_filename = f'capture_{pcap_counter}.pcap'


        save_thread = threading.Thread(target=scapy.utils.wrpcap, args=(pcap_filename, filtered_packets))
        save_thread.start()
        pcap_queue.put(pcap_filename)
        write_event.set()

        pcap_counter += 1
import math
import get_netparam
import get_videoparm
# from common import golbal_qoeParamter
import common
import threading
from decimal import Decimal
from front_end import app

# url = 'http://[2001:250:1001:1044::9d]/testvideo/output.m3u8'

global_lock = threading.Lock()
# apn_ready = 0
len_flag = -1

def QoEScore(pcap_name,m3u8_path):
    # global apn_ready
    parm = [1.26, 4.3, 1.1, 0.8, 0.6, 0.05, 0.35, 0.2]  # miu, omega, niu, eta, alpha, beta, gamma, lambda
    rebuffer_duration_sec = 0  # 卡顿时间
    rebuffer_number = 0  # 卡顿次数
    fei = 1
    Bu = 1  # 视频带宽
    delta = 1
    f_delaytime = 0


    #
    pcap_prase = get_netparam.ScapyPcap(pcap_name)
    #

    netparam = dict(
        lossrate=get_netparam.ScapyPcap(pcap_name).GetLossrate(),
        delay=get_netparam.GetDelay(pcap_name, '2001:250:1001:1044::9d')
    )

    if netparam['lossrate'] < 0:
        netparam['lossrate'] = common.golbal_lossrate
    if netparam['delay'] < 0:
        netparam['delay'] = common.golbal_delay

    ffprobe = get_videoparm.FFprobe()
    ffprobe.parse(m3u8_path)
    print(ffprobe.video_info())

    global len_flag
    len_flag = 1 if get_netparam.ScapyPcap(pcap_name).pktslen > 150 else 0

    app.count_lock.acquire()
    rebuffer_number = app.pause_count
    app.count_lock.release()

    app.time_lock.acquire()
    rebuffer_duration_sec = app.pause_time
    app.time_lock.release()


    videoparam = dict(
        width=ffprobe.video_info()['height_width'][1],
        frame=ffprobe.video_info()['frame_num'],

        # 注意此处的修改------------------------------------------------

        # bitrate=ffprobe.video_info()['bit_rate']
        bitrate = 1536

        # 注意此处的修改------------------------------------------------
    )

    p1 = 3.5 - (3.5 / (1 + (videoparam['bitrate'] / 180)))
    p2 = -(math.pow((math.log(videoparam['frame'], math.e) - math.log(5 + 0.01 * videoparam['bitrate'], math.e)), 2)
           / (2 * math.pow(1.15 + 0.0003 * videoparam['bitrate'], 2)))
    p3 = math.log(0.008 * videoparam['width'], 10)
    p4 = 0.5 * math.log(videoparam['frame'] / 24, 1.1)
    p5 = math.pow(math.log(videoparam['bitrate'], 1000), 5) if videoparam['bitrate'] <= 300 and videoparam['frame'] < 24 \
        else 1
    I_coding = parm[0] * (p1 * math.exp(p2)) * p5 + parm[1] * p3 + p4 * parm[2]

    D_pl = 0.74 - 6.45 * math.exp(-videoparam['frame'] / 0.114) + 13.68 * math.exp(-videoparam['bitrate'] / 513.77)
    P_pl = netparam['lossrate']
    R_pl = math.exp(-P_pl / D_pl)

    r1 = -(0.07 * rebuffer_duration_sec + 0.19) * rebuffer_number
    r2 = 0 if rebuffer_number == 0 else rebuffer_number * 0.2
    I_rebuf = 2 * math.exp(r1) + r2

    I_change = 0
    F_delay = f_delaytime

    if netparam['delay'] is None:
        netparam['delay'] = 0

    QoE_Score = parm[3] * I_coding * R_pl - parm[4] * I_change - parm[5] * F_delay - parm[6] * I_rebuf + fei * Bu - delta * netparam['delay']
    QoE_Score = QoE_Score / 1.2

    global_lock.acquire()
    common.golbal_qoeParamter = [videoparam['width'], videoparam['bitrate'], videoparam['frame'], netparam['lossrate'],
                            rebuffer_duration_sec, rebuffer_number, netparam['delay'], QoE_Score]

    # apn_ready = 1
    global_lock.release()
    
    print("width: ",common.golbal_qoeParamter[0])
    print("bitrate: ",videoparam['bitrate'])
    print("frame: ",videoparam['frame'])
    print("lossrate: ",netparam['lossrate'])
    print("rebuffer_duration_sec: ",rebuffer_duration_sec)
    print("rebuffer_number: ",rebuffer_number)
    print("delaytime: ",netparam['delay'])
    print("cal_qoe: ",QoE_Score)
    print("pcap_nema_cal: ",pcap_name)

    return QoE_Score
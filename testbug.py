
# import subprocess
# import os
# import shutil
# import numpy as np
# import multiprocessing as mp
# from ctypes import *
# from numpy import *
# import QoE_Score
# import threading
# import cal_qoe
# import common
# import time
# from front_end import app
# from datetime import datetime

# addHeader_config_path = "include/ipv6_addHeader_test.so"
# addHeader = CDLL(addHeader_config_path)


# # 获取HLS文件列表
# def get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, apn_value3, request_path, output_path):

#     # print("download start")
#     status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), apn_value1.encode(), apn_value2.encode(), apn_value3.encode(), request_path.encode(), output_path.encode())
#     current_time = datetime.now()
#     formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
#     print("当前系统时间：", formatted_time)
#     # print("status code: ",status)
#     if status != 200:
#         print("Failed to get HLS file list")
#         return []

#     with open(output_path, 'r') as file:
#         content = file.read()  # 读取文件内容
#     lines = content.split('\n')  # 按行分割内容
#     file_list = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
#     return file_list

# def play():

#     interfaceName = "eno1"
#     serverIP = "2001:250:1001:1044::9d"
#     port = 80
#     option_type = 0x3c
#     apn_value1 = "0x1111FFFF"
#     apn_value2 = "0x2222FFFF"
#     apn_value3 = "0x3333FFFF"
#     request_path = "/testvideo/output.m3u8"
#     output_path = "front_end/static/hls_file/output.m3u8"
#     user_category = 2 # 3bit
#     user_gender = 1 # 1bit
#     user_study = 3 # 4bit
#     user_major = 4 # 4bit
#     user_age = 5 # 4bit
#     app_category = 6 # 4bit
#     qoe_int = 0 # 4bit
    
#     bandwidth = 1536 # 4bit
#     delay_unit = 0 # 4bit
#     delay = 0 # 4bit
#     lossrate = 0 # 8bit
#     qoe_float = 0 # 16bit

#     ts_file_num = 0
#     play_end = 0
#     last_lossrate = 0
#     last_delay = 0

#     # 下载TS文件
#     hls_folder = 'front_end/static/hls_file'
#     if not os.path.exists(hls_folder):
#         os.makedirs(hls_folder)


#     apn_value1 = "0b{:03b}{:01b}{:04b}{:04b}{:04b}{:04b}{:04b}{:04b}{:04b}".format(
#     user_category,user_gender,user_study,user_major,user_age,app_category,qoe_int,delay_unit,delay)
#     apn_value1 = apn_value1.replace('-', '')
#     apn_value1 = int(apn_value1, 2)
#     apn_value1 = hex(apn_value1)
#     # apn_value1 = int(apn_value1,16)

#     apn_value2 = "0b{:04b}{:04b}{:08b}{:016b}".format(delay_unit,delay,lossrate,qoe_float)
#     apn_value2 = apn_value2.replace('-', '')
#     apn_value2 = int(apn_value2, 2)
#     apn_value2 = hex(apn_value2)
#     # apn_value2 = int(apn_value2,16)

#     apn_value3 = "0b{:032b}".format(bandwidth)
#     apn_value3 = apn_value3.replace('-', '')
#     apn_value3 = int(apn_value3, 2)
#     apn_value3 = hex(apn_value3)

#     # 获取HLS文件内容
#     file_list = get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2,apn_value3, request_path, output_path)
#     # print('获取HLS文件内容 done')
        

# def main():
#     print("---------------------------V2---------------------------")
#     play()
        

# if __name__=='__main__':
#     # print("start main")
#     main()





# bitrate = 1999
# bitrate_str = int(bitrate / 1000)
# print(bitrate_str)
# bitrate_str = str(bitrate_str)
# bitrate_digits = len(bitrate_str)# ///////////////////////////////////////////////////////
# print(bitrate_digits)

# bitrate = 2 ** 16
# print(bitrate)
# bitrate = bitrate/1000
# print(bitrate)




import math

# from front_end import app

# url = 'http://[2001:250:1001:1044::9d]/testvideo/output.m3u8'

def cal(rebuffer_number,rebuffer_duration_sec):

    # global apn_ready
    parm = [1.26, 4.3, 1.1, 0.8, 0.6, 0.05, 0.35, 0.2]  # miu, omega, niu, eta, alpha, beta, gamma, lambda
    fei = 1
    Bu = 1  # 视频带宽
    delta = 1
    f_delaytime = 0


    #

    #

    netparam = dict(
        lossrate=0,
        delay=0
    )


    videoparam = dict(
        width=1080,
        frame=24,

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
    I_rebuf = 2*math.exp(r1) + r2

    I_change = 0
    F_delay = f_delaytime

    if netparam['delay'] is None:
        netparam['delay'] = 0

    QoE_Score = parm[3] * I_coding * R_pl - parm[4] * I_change - parm[5] * F_delay + parm[6] * I_rebuf + fei * Bu - delta * netparam['delay']
    QoE_Score = QoE_Score / 1.2

    print("rebuffer_number: ",rebuffer_number)
    print("rebuffer_duration_sec: ",rebuffer_duration_sec)
    # print(r1)
    # print(r2)
    print("I_rebuf: ",I_rebuf)
    
    # print(parm[6] * I_rebuf)


    # apn_ready = 1


    # print("bitrate: ",videoparam['bitrate'])
    # print("frame: ",videoparam['frame'])
    # print("lossrate: ",netparam['lossrate'])
    # print("rebuffer_duration_sec: ",rebuffer_duration_sec)
    # print("rebuffer_number: ",rebuffer_number)
    # print("delaytime: ",netparam['delay'])
    print("cal_qoe: ",QoE_Score)
    print("--------------")


cal(0,0)
cal(1,1)
cal(1,2)
cal(1,5)
cal(2,1)
cal(2,2)
cal(2,5)
cal(3,5)
cal(3,7)
cal(3,10)
cal(5,5)
cal(5,10)
cal(5,20)
cal(1,200)
# print(math.exp(-1))
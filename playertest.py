import subprocess
import os
import shutil
import numpy as np
import multiprocessing as mp
from ctypes import *
from numpy import *
import QoE_Score
import threading
import cal_qoe
import common
import time
from front_end import app
from datetime import datetime

addHeader_config_path = "include/ipv6_addHeader.so"
addHeader = CDLL(addHeader_config_path)


# 获取HLS文件列表
def get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, apn_value3,request_path, output_path):

    # print("download start")
    status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), apn_value1.encode(), apn_value2.encode(), apn_value3.encode(),request_path.encode(), output_path.encode())
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("当前系统时间：", formatted_time)
    # print("status code: ",status)
    if status != 200:
        print("Failed to get HLS file list")
        return []

    with open(output_path, 'r') as file:
        content = file.read()  # 读取文件内容
    lines = content.split('\n')  # 按行分割内容
    file_list = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return file_list

# 下载HLS文件
def download_hls_file(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, apn_value3,request_path, output_path):
    # print("download start")
    status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), apn_value1.encode(), apn_value2.encode(), apn_value3.encode(),request_path.encode(), output_path.encode())
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print("222当前系统时间：", formatted_time)
    # print("status code: ",status)
    if status != 200:
        print("Failed to get HLS file list")
        return []

    return True



def play():

    interfaceName = "eno1"
    serverIP = "2001:250:1001:1044::9d"
    port = 80
    option_type = 0x3c
    apn_value1 = "0xFFFFFFFF"
    apn_value2 = "0xFFFFFFFF"
    apn_value3 = "0xFFFFFFFF"
    request_path = "/testvideo/output.m3u8"
    output_path = "front_end/static/hls_file/output.m3u8"
    user_category = 2 # 3bit
    user_gender = 1 # 1bit
    user_study = 3 # 4bit
    user_major = 4 # 4bit
    user_age = 5 # 4bit
    app_category = 6 # 4bit
    qoe_int = 0 # 4bit
    # bandwidth_unit = 2 # 4bit
    bandwidth = 0 # 32bit

    # delay_unit = 0 # 4bit
    delay = 0 # 16bit
    lossrate = 0 # 8bit
    qoe_float = 0 # 16bit

    ts_file_num = 0
    play_end = 0
    last_lossrate = 0
    last_delay = 0

    # 下载TS文件
    hls_folder = 'front_end/static/hls_file'
    if not os.path.exists(hls_folder):
        os.makedirs(hls_folder)


    # 获取HLS文件内容
    file_list = get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2,apn_value3, request_path, output_path)
    # print('获取HLS文件内容 done')


    for i, file in enumerate(file_list):
        # 依次为分辨率、比特率、帧数、丢包率、卡顿持续时间、卡顿次数、延迟、QoE分数
        # print("para_len: ",len(golbal_qoeParamter))
        # print("apn_ready: ", cal_qoe.apn_ready)

        while (i + 1) - ts_file_num > 6:
            app.ts_lock.acquire()
            ts_file_num = app.ts_num
            app.ts_lock.release()
            time.sleep(1)
            
        QoE_Score.apn_lock.acquire()
        apn_is_eady = QoE_Score.apn_ready
        QoE_Score.apn_lock.release()
 
        
        if apn_is_eady > 0:
            cal_qoe.global_lock.acquire()
            # resolution = common.golbal_qoeParamter[0]
            bandwidth = common.golbal_qoeParamter[1]
            # fps = common.golbal_qoeParamter[2]
            lossrate = int(common.golbal_qoeParamter[3])
            # stoptime = common.golbal_qoeParamter[4]
            # stopnum = common.golbal_qoeParamter[5]
            delay = common.golbal_qoeParamter[6]
            qoe_int = int(common.golbal_qoeParamter[7])
            qoe_float = common.golbal_qoeParamter[7] % 1
            cal_qoe.global_lock.release()
            # print("aaaaaa",resolution,bitrate,fps,lossrate,stoptime,stopnum,delay,qoe_int,qoe_float)

            # 信息处理
            
            if qoe_int < 10:
                qoe_float_temp = qoe_float * ( 10 ** 5)
                if qoe_float_temp < 65535:
                    qoe_float = int(qoe_float_temp)
                else:
                    qoe_float  = int(qoe_float * ( 10 ** 4))
            else:
                qoe_int = 9
                qoe_float = 65535
            
            if lossrate < 0:
                lossrate = last_lossrate
            last_lossrate = lossrate

            if delay == 0:
                delay = last_delay
            last_delay = delay

            # ///////////////////////////////////////////////////////
            # bitrate_str = int(bitrate / 1000)
            # bitrate_str = str(bitrate_str)
            # bitrate_digits = len(bitrate_str)
            # if bitrate_digits == 1 & bitrate_str == 0: # if delay < 1ms, see it as zero
            #     delay_unit = 1
            # elif bitrate_digits == 1 & bitrate_str != 0:
            #     pass
            # elif bitrate_digits == 2:
            #     pass
            # elif bitrate_digits == 3:
            #     pass
            # elif bitrate_digits == 4:
            #     pass
            # else: # if delay > 9s, see it as 9s
            #     pass

            # ///////////////////////////////////////////////////////

            delay = int(delay * 1000)
            # delay_str = str(delay)
            # delay_digits = len(delay_str)
            # if delay_digits <= 1: # if delay < 1ms, see it as zero
            #     delay_unit = 1
            # elif delay_digits == 2:
            #     delay_unit = 2
            #     delay = int(delay/10)
            # elif delay_digits == 3:
            #     delay_unit = 4
            #     delay = int(delay/100)
            # elif delay_digits == 4:
            #     delay_unit = 8
            #     delay = int(delay/1000)
            # else: # if delay > 9s, see it as 9s
            #     delay_unit = 8
            #     delay = 9


            print("user_category: ",user_category)
            print("user_gender: ",user_gender)
            print("user_study: ",user_study)
            print("user_major: ",user_major)
            print("user_age: ",user_age)
            print("app_category: ",app_category)
            print("qoe_int: ",qoe_int)
            print("lossrate: ",lossrate)
            print("delay: ",delay)
            print("qoe_float: ",qoe_float)
            print("bandwidth: ",bandwidth)


            apn_value1 = "0b{:03b}{:01b}{:04b}{:04b}{:04b}{:04b}{:04b}{:08b}".format(
                user_category,user_gender,user_study,user_major,user_age,app_category,qoe_int,lossrate)
            apn_value1 = apn_value1.replace('-', '')
            apn_value1 = int(apn_value1, 2)
            apn_value1 = hex(apn_value1)
            # apn_value1 = int(apn_value1,16)

            apn_value2 = "0b{:016b}{:016b}".format(delay,qoe_float)
            apn_value2 = apn_value2.replace('-', '')
            apn_value2 = int(apn_value2, 2)
            apn_value2 = hex(apn_value2)
            # apn_value2 = int(apn_value2,16)

            apn_value3 = "0b{:032b}".format(bandwidth)
            apn_value3 = apn_value3.replace('-', '')
            apn_value3 = int(apn_value3, 2)
            apn_value3 = hex(apn_value3)
        
        
        url = f'{request_path.rsplit("/", 1)[0]}/{file}'
        output_path = os.path.join(hls_folder, f'output{i}.ts')
        print("----------------------------------------download_num: ",i)
        download_hls_file(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, apn_value3, url, output_path)
        # print("cccccapn_value1: ",apn_value1)
        # print("cccccapn_value2: ",apn_value2)
        

    # 清理临时文件
    while play_end == 0:
        app.end_lock.acquire()
        play_end = app.play_end
        app.end_lock.release()
        time.sleep(1)
    shutil.rmtree(hls_folder)
    # os.remove(output_path)
    print('clear flie done')

def main():
    print("---------------------------V1---------------------------")
    
    output_path = 'front_end/static/hls_file/output.m3u8'
    save_thread = threading.Thread(target=QoE_Score.main,args=(output_path,))

    save_thread.start()
    host = '0.0.0.0'
    port = 12396
    player_thread = threading.Thread(target=app.app.run,args=(host, port))
    player_thread.start()
    while True:
        play()
        print("replay")

if __name__=='__main__':
    # print("start main")
    main()


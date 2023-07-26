
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
from front_end import app

addHeader_config_path = "include/ipv6_addHeader.so"
addHeader = CDLL(addHeader_config_path)

# 获取HLS文件列表
def get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, request_path, output_path):

    # print("download start")
    status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), int(apn_value1), int(apn_value2), request_path.encode(), output_path.encode())
    
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
def download_hls_file(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, request_path, output_path):
    # print("download start")
    status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), int(apn_value1), int(apn_value2), request_path.encode(), output_path.encode())
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
    apn_value1 = 0xFFFFFFFF
    apn_value2 = 0xFFFFFFFF
    request_path = "/testvideo/output.m3u8"
    output_path = "front_end/static/hls_file/output.m3u8"
    user_category = 2 # 3bit
    user_gender = 1 # 1bit
    user_study = 3 # 4bit
    user_major = 4 # 4bit
    user_age = 5 # 4bit
    app_category = 6 # 4bit
    qoe_int = 0 # 4bit
    bandwidth_unit = 2 # 4bit
    bandwidth = 1 # 4bit
    delay_unit = 0 # 4bit
    delay = 0 # 4bit
    lossrate = 0 # 8bit
    qoe_float = 0 # 16bit
    


    # 获取HLS文件内容
    file_list = get_hls_file_list(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, request_path, output_path)
    # print('获取HLS文件内容 done')


    # 下载TS文件
    hls_folder = 'front_end/static/hls_file'
    if not os.path.exists(hls_folder):
        os.makedirs(hls_folder)


    for i, file in enumerate(file_list):
        # 依次为分辨率、比特率、帧数、丢包率、卡顿持续时间、卡顿次数、延迟、QoE分数
        # print("para_len: ",len(golbal_qoeParamter))
        # print("apn_ready: ", cal_qoe.apn_ready)
        if cal_qoe.apn_ready > 0:
            cal_qoe.apn_lock.acquire()
            # resolution = common.golbal_qoeParamter[0]
            # bitrate = common.golbal_qoeParamter[1]
            # fps = common.golbal_qoeParamter[2]
            lossrate = int(common.golbal_qoeParamter[3])
            # stoptime = common.golbal_qoeParamter[4]
            # stopnum = common.golbal_qoeParamter[5]
            delay = common.golbal_qoeParamter[6]
            qoe_int = int(common.golbal_qoeParamter[7])
            qoe_float = common.golbal_qoeParamter[7] % 1
            cal_qoe.apn_lock.release()
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
            

            
            delay = int(delay * 1000)
            delay_str = str(delay)
            delay_digits = len(delay_str)
            if delay_digits <= 1: # if delay < 1ms, see it as zero
                delay_unit = 1
            elif delay_digits == 2:
                delay_unit = 2
                delay = int(delay/10)
            elif delay_digits == 3:
                delay_unit = 4
                delay = int(delay/100)
            elif delay_digits == 4:
                delay_unit = 8
                delay = int(delay/1000)
            else: # if delay > 9s, see it as 9s
                delay_unit = 8
                delay = 9

            # print("user_category: ",user_category)
            # print("user_gender: ",user_gender)
            # print("user_study: ",user_study)
            # print("user_major: ",user_major)
            # print("user_age: ",user_age)
            # print("app_category: ",app_category)
            # print("qoe_int: ",qoe_int)
            # print("bandwidth_unit: ",bandwidth_unit)
            # print("bandwidth: ",bandwidth)
            # print("delay_unit: ",delay_unit)
            # print("delay: ",delay)
            # print("lossrate: ",lossrate)
            # print("qoe_float: ",qoe_float)


            apn_value1 = "0b{:03b}{:01b}{:04b}{:04b}{:04b}{:04b}{:04b}{:04b}{:04b}".format(
                user_category,user_gender,user_study,user_major,user_age,app_category,qoe_int,bandwidth_unit,bandwidth)
            apn_value1 = apn_value1.replace('-', '')
            apn_value1 = int(apn_value1, 2)
            apn_value1 = hex(apn_value1)
            apn_value1 = int(apn_value1,16)

            apn_value2 = "0b{:04b}{:04b}{:08b}{:016b}".format(delay_unit,delay,lossrate,qoe_float)
            apn_value2 = int(apn_value2, 2)
            apn_value2 = hex(apn_value2)
            apn_value2 = int(apn_value2,16)
            

        else:
            apn_value1 = 0xFFFFFFFF
            apn_value2 = 0xFFFFFFFF
        
        
        url = f'{request_path.rsplit("/", 1)[0]}/{file}'
        output_path = os.path.join(hls_folder, f'output{i}.ts')
        download_hls_file(interfaceName, serverIP, port, option_type, apn_value1, apn_value2, url, output_path)


    

    # 清理临时文件
    shutil.rmtree(hls_folder)
    # os.remove(output_path)
    print('clear flie done')

def main():
    print("---------------------------V1---------------------------")
    save_thread = threading.Thread(target=QoE_Score.main)
    save_thread.start()
    host = '0.0.0.0'
    port = 12346
    player_thread = threading.Thread(target=app.app.run,args=(host, port))
    player_thread.start()
    while True:
        play()
        print("replay")

if __name__=='__main__':
    # print("start main")
    main()


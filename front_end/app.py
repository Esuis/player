import os
from flask import Flask, render_template, request, jsonify
import threading
import math

app = Flask(__name__)

count_lock = threading.Lock()
time_lock = threading.Lock()
ts_lock = threading.Lock()
end_lock = threading.Lock()
pause_count = 0
pause_time = 0
ts_num = 0
play_end = 0

# # 视频分片所在文件夹路径
# segments_folder = "static/hls_folder/"

# # 视频分片文件名列表（根据实际分片文件名进行修改）
# segment_files = [
#     "output1.ts",
#     "output2.ts",
#     "output3.ts",
#     "output4.ts",
#     "output5.ts",
#     "output6.ts",
#     "output7.ts",
#     "output8.ts"
#     # Add more TS segments as needed
# ]

# # 当前播放分片的索引
# current_segment_index = 0

@app.route('/')
def index():
    return render_template('index.html')

# 暂停次数
@app.route('/update_count', methods=['POST'])
def update_count():
    global pause_count

    data = request.get_json()

    count_lock.acquire()
    pause_count = data.get('pause_count')
    count_lock.release()
    print("pause_count: ",pause_count)

    return jsonify({'message': 'count updated successfully'})

#暂停时长
@app.route('/update_time', methods=['POST'])
def update_time():
    global pause_time

    data = request.get_json()
    
    time_lock.acquire()
    pause_time = data.get('pause_time')
    if pause_time > 1000:
        pause_time = 0
    time_lock.release()
    print("pause_time: ",pause_time)

    return jsonify({'message': 'time updated successfully'})

#播放时长，用于计算当前播到第几个ts文件
@app.route('/update_nowtime', methods=['POST'])
def update_nowtime():
    global ts_num

    data = request.get_json()
    play_time = data.get('now_play_time')
    
    ts_lock.acquire()
    ts_num = math.ceil(play_time/9)
    ts_lock.release()

    print("ts_num: ",ts_num)

    return jsonify({'message': 'now_play_time updated successfully'})

#播放结束
@app.route('/update_ended', methods=['POST'])
def update_ended():
    global play_end

    data = request.get_json()
    end_lock.acquire()
    play_end = data.get('play_end')
    end_lock.release()

    print("play_end: ",play_end)

    return jsonify({'message': 'now_play_time updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13010)

import os
from flask import Flask, render_template, request, jsonify
import threading

app = Flask(__name__)

count_lock = threading.Lock()
time_lock = threading.Lock()
pause_count = 0
pause_time = 0

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

@app.route('/update_count', methods=['POST'])
def update_count():
    global pause_count

    data = request.get_json()

    count_lock.acquire()
    pause_count = data.get('pause_count')
    count_lock.release()
    print("pause_count: ",pause_count)

    return jsonify({'message': 'count updated successfully'})

@app.route('/update_time', methods=['POST'])
def update_time():
    global pause_time

    data = request.get_json()
    
    time_lock.acquire()
    pause_time = data.get('pause_time')
    time_lock.release()
    print("pause_time: ",pause_time)

    return jsonify({'message': 'time updated successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5040)

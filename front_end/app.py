import os
from flask import Flask, render_template

app = Flask(__name__)

# 视频分片所在文件夹路径
segments_folder = "static/hls_folder/"

# 视频分片文件名列表（根据实际分片文件名进行修改）
segment_files = [
    "output1.ts",
    "output2.ts",
    "output3.ts",
    "output4.ts",
    "output5.ts",
    "output6.ts",
    "output7.ts",
    "output8.ts"
    # Add more TS segments as needed
]

# 当前播放分片的索引
current_segment_index = 0

@app.route('/')
def index():
    global current_segment_index
    current_segment_file = os.path.join(segments_folder, segment_files[current_segment_index])
    next_segment_file = os.path.join(segments_folder, segment_files[(current_segment_index + 1) % len(segment_files)])

    return render_template('index.html', current_segment_file=current_segment_file, next_segment_file=next_segment_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5019)

import os
import sys
import cv2
import threading
import queue

def play_video(ts_file_queue):
    while True:
        ts_file = ts_file_queue.get()
        if ts_file is None:
            break

        cap = cv2.VideoCapture(ts_file)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            sys.exit(1)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("TS Video Player", frame)
            if cv2.waitKey(30) & 0xFF == 27:  # 按ESC键退出
                break

        cap.release()

    cv2.destroyAllWindows()

def main():
    ts_files = ["hls_folder/1.ts", "hls_folder/2.ts", "hls_folder/3.ts", "hls_folder/4.ts", "hls_folder/5.ts", "hls_folder/6.ts", "hls_folder/7.ts", "hls_folder/8.ts"]  # 替换为您的.ts文件列表

    ts_file_queue = queue.Queue()
    for ts_file in ts_files:
        ts_file_queue.put(ts_file)

    cv2.namedWindow("TS Video Player", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TS Video Player", 1792, 768)

    # 启动播放线程
    play_thread = threading.Thread(target=play_video, args=(ts_file_queue,), daemon=True)
    play_thread.start()

    play_thread.join()  # 等待播放线程结束

if __name__ == "__main__":
    main()

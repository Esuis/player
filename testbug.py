# import os
# import sys
# import cv2
# import threading
# import queue

# def play_video(ts_file_queue):
#     while True:
#         ts_file = ts_file_queue.get()
#         if ts_file is None:
#             break

#         cap = cv2.VideoCapture(ts_file)
#         if not cap.isOpened():
#             print("Error: Unable to open video file.")
#             sys.exit(1)
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             cv2.imshow("TS Video Player", frame)
#             if cv2.waitKey(30) & 0xFF == 27:  # 按ESC键退出
#                 break

#         cap.release()

#     cv2.destroyAllWindows()

# def main():
#     ts_files = ["../lwh_file/hls_folder/output1.ts", "../lwh_file/hls_folder/output2.ts", "../lwh_file/hls_folder/output3.ts", "../lwh_file/hls_folder/output4.ts", "../lwh_file/hls_folder/output5.ts", "../lwh_file/hls_folder/output6.ts", "../lwh_file/hls_folder/output7.ts", "../lwh_file/hls_folder/output8.ts"]  # 替换为您的.ts文件列表

#     ts_file_queue = queue.Queue()
#     for ts_file in ts_files:
#         ts_file_queue.put(ts_file)

#     cv2.namedWindow("TS Video Player", cv2.WINDOW_NORMAL)
#     cv2.resizeWindow("TS Video Player", 1728, 720)

#     # 启动播放线程
#     play_thread = threading.Thread(target=play_video, args=(ts_file_queue,), daemon=True)
#     play_thread.start()

#     play_thread.join()  # 等待播放线程结束

# if __name__ == "__main__":
#     main()








import vlc

def play_ts_files(ts_files):
    player = vlc.Instance('--no-xlib', '--file-caching=1000', '--network-caching=1000', '--live-caching=1000', '--avcodec-hw=any')
    media_list = player.media_list_new()

    for ts_file in ts_files:
        media = player.media_new(ts_file)
        media_list.add_media(media)

    player = player.media_list_player_new()
    player.set_media_list(media_list)
    player.play()

    while True:
        pass




if __name__ == "__main__":
    ts_files = ["/home/nskeylab/lwh_file/hls_folder/output1.ts", "/home/nskeylab/lwh_file/hls_folder/output2.ts", "/home/nskeylab/lwh_file/hls_folder/output3.ts", "/home/nskeylab/lwh_file/hls_folder/output4.ts", "/home/nskeylab/lwh_file/hls_folder/output5.ts", "/home/nskeylab/lwh_file/hls_folder/output6.ts", "/home/nskeylab/lwh_file/hls_folder/output7.ts", "/home/nskeylab/lwh_file/hls_folder/output8.ts"]   # Replace with your list of TS files
    play_ts_files(ts_files)

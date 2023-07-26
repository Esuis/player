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








# import vlc

# def play_ts_files(ts_files):
#     player = vlc.Instance('--no-xlib', '--file-caching=1000', '--network-caching=1000', '--live-caching=1000', '--avcodec-hw=any')
#     media_list = player.media_list_new()

#     for ts_file in ts_files:
#         media = player.media_new(ts_file)
#         media_list.add_media(media)

#     player = player.media_list_player_new()
#     player.set_media_list(media_list)
#     player.play()

#     while True:
#         pass




# if __name__ == "__main__":
#     ts_files = ["/home/nskeylab/lwh_file/hls_folder/output1.ts", "/home/nskeylab/lwh_file/hls_folder/output2.ts", "/home/nskeylab/lwh_file/hls_folder/output3.ts", "/home/nskeylab/lwh_file/hls_folder/output4.ts", "/home/nskeylab/lwh_file/hls_folder/output5.ts", "/home/nskeylab/lwh_file/hls_folder/output6.ts", "/home/nskeylab/lwh_file/hls_folder/output7.ts", "/home/nskeylab/lwh_file/hls_folder/output8.ts"]   # Replace with your list of TS files
#     play_ts_files(ts_files)





# import vlc
# import threading
# import time

# # Replace with your list of TS segments
# ts_segments = [
#     "/home/nskeylab/lwh_file/hls_folder/output1.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output2.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output3.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output4.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output5.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output6.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output7.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output8.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output9.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output10.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output11.ts",
#     # Add more TS segments as needed
# ]

# def play_next_segment(media_list_player, current_index):
#     next_index = current_index + 1
#     if next_index < len(ts_segments):
#         media = vlc_instance.media_new(ts_segments[next_index])
#         media_list_player.get_media_player().set_media(media)
#         media_list_player.play_item_at_index(next_index)

# # Initialize VLC instance and media player
# # vlc_instance = vlc.Instance()
# vlc_instance = vlc.Instance('--no-xlib --ffmpeg-hw --file-caching=2000')
# # vlc_instance = vlc.Instance('--no-xlib')
# media_player = vlc_instance.media_player_new()

# # Create a media list player to handle the TS segments
# media_list_player = vlc_instance.media_list_player_new()

# # Create a media list to hold the TS segments
# media_list = vlc_instance.media_list_new(ts_segments)

# # Set the media list to the media list player
# media_list_player.set_media_list(media_list)

# # Set the media player to the media list player
# media_list_player.set_media_player(media_player)

# # Start playing the first segment
# media_list_player.play()

# # Start a separate thread to handle preloading of the next segment
# current_index = 0
# preload_thread = threading.Thread(target=play_next_segment, args=(media_list_player, current_index))
# preload_thread.start()

# try:
#     while True:
#         time.sleep(0.1)  # Adjust the sleep time based on your requirements
#         # Check if the current segment has finished playing
#         if media_player.get_state() == vlc.State.Ended:
#             current_index += 1
#             if current_index < len(ts_segments):
#                 # Start preloading the next segment in a new thread
#                 preload_thread = threading.Thread(target=play_next_segment, args=(media_list_player, current_index))
#                 preload_thread.start()

# except KeyboardInterrupt:
#     # Handle keyboard interrupt (Ctrl+C) to stop the player
#     media_list_player.stop()










# import vlc
# import threading
# import time

# # Replace with your list of TS segments
# ts_segments = [
#     "/home/nskeylab/lwh_file/hls_folder/output1.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output2.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output3.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output4.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output5.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output6.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output7.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output8.ts",
#     "/home/nskeylab/lwh_file/hls_folder/output9.ts"
#     # Add more TS segments as needed
# ]

# def preload_next_segment(media_list_player, current_index):
#     next_index = current_index + 1
#     if next_index < len(ts_segments):
#         media = vlc_instance.media_new(ts_segments[next_index])
#         media_list_player.get_media_player().set_media(media)
#         media_list_player.play_item_at_index(next_index)

# def play_next_segment(media_list_player, current_index):
#     next_index = current_index + 1
#     if next_index + 1 < len(ts_segments):
#         preload_thread = threading.Thread(target=preload_next_segment, args=(media_list_player, next_index))
#         preload_thread.start()

# # Initialize VLC instance and media player
# # vlc_instance = vlc.Instance("--clock-synchro 0 --no-hardware-accel --file-caching=10000")
# vlc_instance = vlc.Instance("--no-xlib --file-caching=10000")
# media_player = vlc_instance.media_player_new()

# # Create a media list player to handle the TS segments
# media_list_player = vlc_instance.media_list_player_new()

# # Create a media list to hold the TS segments
# media_list = vlc_instance.media_list_new(ts_segments)

# # Set the media list to the media list player
# media_list_player.set_media_list(media_list)

# # Set the media player to the media list player
# media_list_player.set_media_player(media_player)

# # Start playing the first segment
# media_list_player.play()

# # Start preloading the next two segments in a new thread
# current_index = 0
# preload_thread = threading.Thread(target=preload_next_segment, args=(media_list_player, current_index))
# preload_thread.start()
# play_next_thread = threading.Thread(target=play_next_segment, args=(media_list_player, current_index))
# play_next_thread.start()

# try:
#     while True:
#         time.sleep(0.01)  # Adjust the sleep time based on your requirements
#         # Check if the current segment has finished playing
#         if media_player.get_state() == vlc.State.Ended:
#             current_index += 1
#             if current_index < len(ts_segments):
#                 # Start preloading the next segment in a new thread
#                 preload_thread = threading.Thread(target=preload_next_segment, args=(media_list_player, current_index))
#                 preload_thread.start()
#                 # Start playing the next segment in a new thread
#                 play_next_thread = threading.Thread(target=play_next_segment, args=(media_list_player, current_index))
#                 play_next_thread.start()

# except KeyboardInterrupt:
#     # Handle keyboard interrupt (Ctrl+C) to stop the player
#     media_list_player.stop()



# import vlc

# # 创建VLC实例
# vlc_instance = vlc.Instance("--no-xlib --file-caching=10000")

# # 创建MediaListPlayer对象
# media_list_player = vlc_instance.media_list_player_new()

# # 创建MediaList对象并添加本地M3U8文件
# media_list = vlc_instance.media_list_new()
# m3u8_file_path = "/home/nskeylab/lwh_file/hls_folder/output.m3u8"
# media = vlc_instance.media_new_path(m3u8_file_path)
# media_list.add_media(media)

# # 设置MediaList到MediaListPlayer
# media_list_player.set_media_list(media_list)

# # 获取MediaPlayer对象
# media_player = media_list_player.get_media_player()

# # 开始播放本地M3U8文件
# media_list_player.play()

# # 等待播放结束
# while True:
#     pass



import subprocess

# 本地M3U8文件路径
m3u8_file_path = "/home/nskeylab/lwh_file/hls_folder/output.m3u8"

# 使用subprocess运行ffplay命令
ffplay_cmd = f"ffplay {m3u8_file_path}"
subprocess.run(ffplay_cmd, shell=True)

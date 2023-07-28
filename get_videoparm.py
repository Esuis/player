import subprocess
import json
import fractions
import requests


class FFprobe():
    def __init__(self):
        self.filepath = ''
        self._video_info = {}

    def parse(self, filepath):
        self.filepath = filepath
        try:
            res = subprocess.check_output(['ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format', '-show_streams', '-v','quiet'])
            res = res.decode('utf8')
            self._video_info = json.loads(res)
            print(self._video_info)
        except Exception as e:
            print(e)
            raise Exception('获取视频信息失败')

    def video_width_height(self):
        streams = self._video_info['streams'][0]
        if 'width' in streams:
            return (streams['width'], streams['height'])
        elif 'width' in self._video_info['streams'][1]:
            return (self._video_info['streams'][1]['width'], self._video_info['streams'][1]['height'])
        else:
            return -1

    def video_filesize(self, format='gb'):
        v_format = self._video_info['format']
        size = int(v_format['size'])
        kb = 1024
        mb = kb * 1024
        gb = mb * 1024
        tb = gb * 1024
        if size >= tb:
            return "%.1f TB" % float(size / tb)
        if size >= gb:
            return "%.1f GB" % float(size / gb)
        if size >= mb:
            return "%.1f MB" % float(size / mb)
        if size >= kb:
            return "%.1f KB" % float(size / kb)

    def video_frame(self):
        stream = self._video_info['streams'][0]
        if stream['r_frame_rate'] != '0/0':
            frac = fractions.Fraction(str(stream['r_frame_rate']))
            frame_rate = frac.numerator / frac.denominator
        else:
            frame_rate = -1
        return frame_rate

    def video_time_length(self):
        v_format = self._video_info['format']
        return str(int(float(v_format['duration']) / 3600)).__add__('小时').__add__(
            str(int(float(v_format['duration']) % 3600 / 60))).__add__('分钟')

    def video_bitrate(self, filepath):
        self.filepath = filepath

        # 发起请求获取M3U8文件内容
        m3u8_content = self.filepath
        

        # 分割M3U8文件内容为行
        lines = m3u8_content.split('\n')

        # 初始化变量
        video_bitrate = None

        # 遍历每一行内容
        for line in lines:
            # 查找视频流信息行
            if line.startswith('#EXT-X-STREAM-INF'):
                # 提取码率
                bitrate_start = line.find('AVERAGE-BANDWIDTH=') + len('AVERAGE-BANDWIDTH=')
                bitrate_end = line.find(',', bitrate_start)
                video_bitrate = line[bitrate_start:bitrate_end]

                # 找到第一个匹配的视频流信息行后，结束循环
                break

        return 2000 if video_bitrate is None else video_bitrate

    def video_info(self):
        item = {
            'height_width': self.video_width_height(),
            'filesize': self.video_filesize(),
            'time_length': self.video_time_length(),
            'frame_num': self.video_frame(),
            'bit_rate': self.video_bitrate(self.filepath)
        }
        print('视频参数为 = ', item)
        return item


# url = "/home/nskeylab/lwh/output.m3u8"
# if __name__ == "__main__":
#     ffprobe = FFprobe()
#     ffprobe.parse(url)
#     print(ffprobe.video_info())

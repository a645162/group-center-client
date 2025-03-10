# pip install li-group-center

# OpenCV push to RTSP Server example
# Author: Haomin Kong
import time

import cv2
import numpy as np  # 添加numpy导入 / Add numpy import

from group_center.tools.rtsp.rtsp_push import RtspPush

video_path: str = "test.mp4"  # 视频文件路径 / Video file path
server_url: str = r""  # RTSP服务器地址 / RTSP server URL
loop: bool = True  # 是否循环播放 / Whether to loop playback

cap: cv2.VideoCapture = cv2.VideoCapture(
    video_path
)  # 视频捕获对象 / Video capture object

# Get video information / 获取视频信息
ret: bool
frame: np.ndarray
ret, frame = cap.read()
if not ret:
    print("Can't read video")  # 无法读取视频 / Unable to read video
    exit()

height: int
width: int
layers: int
height, width, layers = frame.shape  # 视频尺寸 / Video dimensions
fps: float = cap.get(cv2.CAP_PROP_FPS)  # 视频帧率 / Video frame rate

pusher: RtspPush = RtspPush(
    rtsp_url=server_url, width=width, height=height, fps=fps
)  # RTSP推流器 / RTSP pusher
pusher.set_encoder_gpu_amd()  # 设置AMD GPU编码器 / Set AMD GPU encoder

if not pusher.open():  # 打开推流器 / Open pusher
    print("Can't open pusher")  # 无法打开推流器 / Unable to open pusher
    exit(1)

try:
    count: int = 0  # 帧计数器 / Frame counter
    while True:
        ret, frame = cap.read()
        if not ret:
            # If the end of the video is reached, you can choose to exit or restart (loop playback)
            # 如果到达视频结尾，可以选择退出或重新开始（循环播放）
            if not loop:
                break

            # Restart playback / 重新开始播放
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            count = 0

            # Continue to the next iteration of the loop / 继续下一次循环
            continue

        count += 1

        start_time: float = time.time()  # 记录开始时间 / Record start time

        # Add text / 添加文字
        cv2.putText(
            frame,
            f"Frame:{count}",  # 显示当前帧数 / Display current frame count
            (50, 50),  # 文字位置 / Text position
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体 / Font
            2,  # 字体大小 / Font scale
            (0, 0, 255),  # 文字颜色（红色） / Text color (red)
            2,  # 文字厚度 / Text thickness
        )

        pusher.push(frame)  # 推送帧 / Push frame

except KeyboardInterrupt:
    print("KeyboardInterrupt")  # 捕获键盘中断 / Catch keyboard interrupt

finally:
    pusher.close()  # 关闭推流器 / Close pusher

    cap.release()  # 释放视频捕获 / Release video capture
    cv2.destroyAllWindows()  # 销毁所有OpenCV窗口 / Destroy all OpenCV windows

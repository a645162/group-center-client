# pip install li-group-center

# Pillow push to RTSP Server example
# Author: Haomin Kong
import datetime

from PIL import Image, ImageDraw

from group_center.tools.rtsp.rtsp_push import RtspPush

height: int = 480  # 视频高度 / Video height
width: int = 640  # 视频宽度 / Video width
server_url: str = r""  # RTSP服务器地址 / RTSP server URL
fps: int = 30  # 帧率 / Frame rate

pusher: RtspPush = RtspPush(
    rtsp_url=server_url, width=width, height=height, fps=fps
)  # RTSP推流器 / RTSP pusher
pusher.set_encoder_gpu_amd()  # 设置AMD GPU编码器 / Set AMD GPU encoder

base_image: Image.Image = Image.new(
    "RGB", (width, height), color="white"
)  # 基础图像 / Base image

pusher.open()  # 打开推流器 / Open pusher

try:
    while True:
        current_image: Image.Image = (
            base_image.copy()
        )  # 创建当前帧图像 / Create current frame image

        # Write Text / 写入文字
        current_time: str = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # 当前时间 / Current time
        text: str = f"Current Time: {current_time}"  # 显示文本 / Display text
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(
            current_image
        )  # 创建绘图对象 / Create drawing object
        draw.text((50, 50), text, fill="red")  # 在图像上绘制文字 / Draw text on image
        del draw  # 删除绘图对象 / Delete drawing object

        pusher.push_pillow(current_image)  # 推送Pillow图像帧 / Push Pillow image frame
except KeyboardInterrupt:
    print("KeyboardInterrupt")  # 捕获键盘中断 / Catch keyboard interrupt
finally:
    pusher.close()  # 关闭推流器 / Close pusher
    print("Done")  # 完成提示 / Done notification

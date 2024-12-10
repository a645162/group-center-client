# pip install li-group-center

# Pillow push to RTSP Server example
# Author: Haomin Kong
import datetime

from PIL import Image, ImageDraw

from group_center.tools.rtsp.rtsp_push import RtspPush

height = 480
width = 640
server_url = r""
fps = 30

pusher = RtspPush(
    rtsp_url=server_url,
    width=width,
    height=height,
    fps=fps
)
pusher.set_encoder_gpu_amd()

base_image = Image.new('RGB', (width, height), color='white')

pusher.open()

try:
    while True:
        current_image = base_image.copy()

        # Write Text
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"Current Time: {current_time}"
        draw = ImageDraw.Draw(current_image)
        draw.text((50, 50), text, fill='red')
        del draw

        pusher.push_pillow(current_image)
except KeyboardInterrupt:
    print('KeyboardInterrupt')
finally:
    pusher.close()
    print('Done')

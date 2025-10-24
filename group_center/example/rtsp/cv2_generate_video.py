# 生成10秒的视频，每一秒都在左上角显示当前的秒数
# Generate a 10-second video, displaying the current second in the top-left corner each second
from typing import Tuple

import cv2
import numpy as np
import tqdm

path: str = "test.mp4"  # 输出视频路径 / Output video path

fps: int = 30  # 帧率 / Frame rate
sec: int = 20  # 视频时长（秒） / Video duration (seconds)
total_frame: int = fps * sec  # 总帧数 / Total frames

size: Tuple[int, int] = (640, 480)  # 视频分辨率 / Video resolution
fourcc: int = cv2.VideoWriter_fourcc(*"XVID")  # 视频编码 / Video codec
videoWriter: cv2.VideoWriter = cv2.VideoWriter(
    path, fourcc, fps, size
)  # 视频写入器 / Video writer
for i in tqdm.tqdm(range(total_frame)):
    # 创建白色画布 / Create white canvas
    img: np.ndarray = 255 * np.ones((size[1], size[0], 3), dtype=np.uint8)

    position_center: Tuple[int, int] = (
        size[0] // 2,
        size[1] // 2,
    )  # 中心位置 / Center position

    # 在左上角写入秒数 / Write seconds in top-left corner
    cv2.putText(
        img, str(i // fps), position_center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2
    )
    videoWriter.write(img)  # 写入帧 / Write frame

videoWriter.release()  # 释放视频写入器 / Release video writer

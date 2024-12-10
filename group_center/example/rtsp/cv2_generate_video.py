# 生成10秒的视频，每一秒都在左上角显示当前的秒数
import cv2
import numpy as np
import tqdm

path = "test.mp4"

fps = 30
sec = 20
total_frame = fps * sec

size = (640, 480)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriter = cv2.VideoWriter(path, fourcc, fps, size)
for i in tqdm.tqdm(range(total_frame)):
    # 创建白色画布
    img = 255 * np.ones((size[1], size[0], 3), dtype=np.uint8)

    position_center=(size[0]//2, size[1]//2)

    # 在左上角写入秒数
    cv2.putText(img, str(i // fps), position_center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    videoWriter.write(img)

videoWriter.release()

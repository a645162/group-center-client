# pip install li-group-center

# OpenCV push to RTSP Server example
# Author: Haomin Kong
import time

import cv2

from group_center.tools.rtsp.rtsp_push import RtspPush

video_path = "test.mp4"
server_url = r""
loop = True

cap = cv2.VideoCapture(video_path)

# Get video information
ret, frame = cap.read()
if not ret:
    print("Can't read video")
    exit()

height, width, layers = frame.shape
fps = cap.get(cv2.CAP_PROP_FPS)

pusher = RtspPush(
    rtsp_url=server_url,
    width=width,
    height=height,
    fps=fps
)
pusher.set_encoder_gpu_amd()

if not pusher.open():
    print("Can't open pusher")
    exit(1)

try:
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            # If the end of the video is reached, you can choose to exit or restart (loop playback)
            if not loop:
                break

            # Restart playback
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            count = 0

            # Continue to the next iteration of the loop
            continue

        count += 1

        start_time = time.time()

        # Add text
        cv2.putText(
            frame,
            f"Frame:{count}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            2
        )

        pusher.push(frame)

except KeyboardInterrupt:
    print('KeyboardInterrupt')

finally:
    pusher.close()

    cap.release()
    cv2.destroyAllWindows()

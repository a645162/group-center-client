import subprocess as sp
import time
from typing import List, Optional
import platform

import numpy as np


class RtspPush:
    """RTSP 推流类
    RTSP Push Class

    用于通过RTSP协议推送视频流
    Used to push video stream via RTSP protocol
    """

    __rtst_url: str = ""
    __opened: bool = False

    __command: List[str]
    __params_encoder: List[str]
    __width: int
    __height: int
    __fps: float

    __last_time: Optional[time.time] = None

    __p: Optional[sp.Popen] = None

    interval: bool = True

    __open_have_error: bool = False

    def __init__(
        self,
        rtsp_url: str,
        width: int = 1920,
        height: int = 1080,
        fps: float = 30,
        interval: bool = True,
    ):
        """初始化RTSP推流实例
        Initialize RTSP push instance

        Args:
            rtsp_url (str): RTSP服务器地址
            rtsp_url (str): RTSP server URL
            width (int, optional): 视频宽度. Defaults to 1920.
            width (int, optional): Video width. Defaults to 1920.
            height (int, optional): 视频高度. Defaults to 1080.
            height (int, optional): Video height. Defaults to 1080.
            fps (float, optional): 帧率. Defaults to 30.
            fps (float, optional): Frame rate. Defaults to 30.
            interval (bool, optional): 是否启用帧间隔控制. Defaults to True.
            interval (bool, optional): Whether to enable frame interval control. Defaults to True.
        """
        self.__rtst_url = rtsp_url

        self.__command = []
        self.__params_encoder = []

        self.__width = width
        self.__height = height
        self.__fps = fps
        self.interval = interval

        self.set_recommend_encoder()

        self.update_command()

    @staticmethod
    def check() -> bool:
        # Check is ffmpeg installed
        try:
            sp.run(["ffmpeg", "-version"], capture_output=True)

            return True
        except FileNotFoundError:
            print("ffmpeg not found")
            return False
        except sp.CalledProcessError:
            print("ffmpeg can't run")
            return False
        except Exception as e:
            print(e)
            return False

    @property
    def is_opened(self) -> bool:
        """检查推流是否已开启
        Check if streaming is opened

        Returns:
            bool: 推流是否已开启
            bool: Whether streaming is opened
        """
        return self.__opened

    @property
    def rtsp_url(self) -> str:
        """获取RTSP服务器地址
        Get RTSP server URL

        Returns:
            str: RTSP服务器地址
            str: RTSP server URL
        """
        return self.__rtst_url

    @property
    def width(self) -> int:
        """获取视频宽度
        Get video width

        Returns:
            int: 视频宽度
            int: Video width
        """
        return self.__width

    @width.setter
    def width(self, width: int):
        if self.is_opened:
            return

        self.__width = width

        self.update_command()

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        if self.is_opened:
            return

        self.__height = height

        self.update_command()

    @property
    def fps(self) -> float:
        """获取视频帧率
        Get video frame rate

        Returns:
            float: 视频帧率
            float: Video frame rate
        """
        return self.__fps

    @fps.setter
    def fps(self, fps: float):
        if self.is_opened:
            return

        self.__fps = fps

        self.update_command()

    def set_recommend_encoder(self) -> None:
        """根据系统硬件自动推荐编码器
        Automatically recommend encoder based on system hardware

        该方法会检测系统GPU类型并设置相应的编码器
        This method detects system GPU type and sets corresponding encoder
        """
        """Set recommended video encoder based on detected hardware"""
        # Is Linux
        if self.is_linux():
            # Get GPU List
            gpu_text = sp.run(["lspci", "-v"], capture_output=True, text=True).stdout

            # Check Intel GPU
            # if "Intel Corporation" in gpu_text:
            #     self.set_encoder_gpu_intel()

            # Check Nvidia GPU
            if "NVIDIA Corporation" in gpu_text:
                self.set_encoder_gpu_nvidia()

            # Check AMD GPU
            if "Advanced Micro Devices, Inc." in gpu_text:
                self.set_encoder_gpu_amd()

        elif self.is_macos():
            self.set_encoder_cpu()
        else:
            self.set_encoder_cpu()

    def set_encoder_cpu(self) -> None:
        """设置CPU编码器参数
        Set CPU encoder parameters

        该方法会设置使用CPU进行视频编码的参数
        This method sets parameters for CPU video encoding
        """
        self.__params_encoder = [
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
        ]

    def set_encoder_gpu_intel(self) -> None:
        """设置Intel GPU编码器参数/Set Intel GPU encoder parameters"""
        self.__params_encoder = [
            "-c:v",
            "h264_qsv",
        ]
        self.update_command()

    def set_encoder_gpu_nvidia(self) -> None:
        self.__params_encoder = [
            "-c:v",
            "h264_nvenc",
        ]

        self.update_command()

    def set_encoder_gpu_amd(self) -> None:
        self.__params_encoder = [
            "-c:v",
            "h264_amf",
        ]

        self.update_command()

    def update_command(self):
        width = self.width
        height = self.height
        fps = self.fps

        rtsp_url = self.rtsp_url

        default_encoder = [
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
        ]

        params_encoder = self.__params_encoder.copy()
        if len(params_encoder) == 0:
            params_encoder = default_encoder

        command = [
            "ffmpeg",
            "-y",  # 覆盖输出文件而不询问
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            "{}x{}".format(width, height),
            "-r",
            str(fps),  # 帧率
            "-i",
            "-",  # 输入来自标准输入
            *params_encoder,
            "-pix_fmt",
            "yuv420p",
            "-rtsp_transport",
            "tcp",
            "-f",
            "rtsp",
            rtsp_url,
        ]

        self.__command = command

    def open(self) -> bool:
        try:
            self.update_command()
            command = self.__command
            self.__p = sp.Popen(command, stdin=sp.PIPE)

            self.__opened = True

            return True
        except Exception as e:
            print(e)

            self.__open_have_error = True
            self.__opened = False

            return False

    def close(self):
        if self.is_opened:
            try:
                self.__p.stdin.close()

                self.__open_have_error = False
                self.__opened = False
            except Exception as e:
                print(e)

    def __before_push(self) -> bool:
        if not self.is_opened:
            # If last open not have error, try open again
            if not self.__open_have_error:
                if self.open():
                    return True

            return False

        return True

    def push_cv2(self, frame: np.ndarray) -> None:
        if not self.__before_push():
            return

        if self.interval and self.__last_time is not None:
            elapsed_time = time.time() - self.__last_time
            frame_interval = 1 / self.fps
            if elapsed_time < frame_interval:
                time.sleep(frame_interval - elapsed_time)

        try:
            self.__p.stdin.write(frame.tobytes())
        except Exception as e:
            print(e)

        self.__last_time = time.time()

    def push_pillow(self, image: Image.Image, convert_to_bgr: bool = True) -> None:
        if not self.__before_push():
            return

        cv2_data = np.array(image)

        if convert_to_bgr:
            # Convert to BGR format
            cv2_data = cv2_data[:, :, ::-1]

        self.push_cv(cv2_data)

    push_cv = push_cv2
    push = push_cv

    def install(self) -> bool:
        if self.check():
            print("ffmpeg is installed")
            return True
        elif self.is_linux():
            # sudo apt install ffmpeg -y
            command = "sudo apt install ffmpeg -y"
            sp.run(command, shell=True)
            return self.check()
        elif self.is_windows():
            print("Installer is not implemented on Windows")
        else:
            print("Unknown OS")

    @staticmethod
    def is_linux() -> bool:
        return platform.system() == "Linux"

    @staticmethod
    def is_windows() -> bool:
        return platform.system() == "Windows"

    @staticmethod
    def is_macos() -> bool:
        return platform.system() == "Darwin"

    def __del__(self):
        self.close()

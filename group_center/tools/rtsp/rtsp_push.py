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

    __rtst_url: str = ""  # RTSP服务器URL地址 / RTSP server URL address
    __opened: bool = (
        False  # 推流是否已开启的标志 / Flag indicating whether streaming is opened
    )

    __command: List[str]  # FFmpeg命令行参数列表 / List of FFmpeg command line arguments
    __params_encoder: List[str]  # 编码器参数列表 / List of encoder parameters
    __width: int  # 视频宽度（像素） / Video width (pixels)
    __height: int  # 视频高度（像素） / Video height (pixels)
    __fps: float  # 视频帧率 / Video frame rate

    __last_time: Optional[time.time] = (
        None  # 上一帧发送时间，用于控制帧率 / Time of last frame sent, used for frame rate control
    )

    __p: Optional[sp.Popen] = None  # FFmpeg进程对象 / FFmpeg process object

    interval: bool = (
        True  # 是否启用帧间隔控制 / Whether to enable frame interval control
    )

    __open_have_error: bool = (
        False  # 上次打开过程是否发生错误 / Whether an error occurred during the last open attempt
    )

    def __init__(
        self,
        rtsp_url: str,  # RTSP服务器地址，用于推流的目标URL / RTSP server URL, the destination URL for streaming
        width: int = 1920,  # 视频宽度(像素)，定义推流画面的宽度 / Video width(pixels), defines the width of streaming video
        height: int = 1080,  # 视频高度(像素)，定义推流画面的高度 / Video height(pixels), defines the height of streaming video
        fps: float = 30,  # 帧率，每秒传输的视频帧数 / Frame rate, number of video frames transmitted per second
        interval: bool = True,  # 是否启用帧间隔控制，用于限制帧率 / Whether to enable frame interval control, used to limit frame rate
    ):
        """初始化RTSP推流实例
        Initialize RTSP push instance

        创建一个RTSP推流实例，设置视频参数并准备推流环境
        Create an RTSP streaming instance, set video parameters and prepare the streaming environment

        Args:
            rtsp_url (str): RTSP服务器地址，如rtsp://server:port/stream /
                RTSP server URL, like rtsp://server:port/stream
            width (int, optional): 视频宽度(像素)，默认为1920 /
                Video width(pixels), defaults to 1920
            height (int, optional): 视频高度(像素)，默认为1080 /
                Video height(pixels), defaults to 1080
            fps (float, optional): 帧率，每秒传输的帧数，默认为30 /
                Frame rate, frames transmitted per second, defaults to 30
            interval (bool, optional): 是否启用帧间隔控制，用于稳定帧率，默认为True /
                Whether to enable frame interval control for stable frame rate, defaults to True
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
        """检查系统是否安装了ffmpeg
        Check if ffmpeg is installed on the system

        Returns:
            bool: ffmpeg是否可用 / Whether ffmpeg is available
        """
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
            bool: 推流是否已开启 / Whether streaming is opened
        """
        return self.__opened

    @property
    def rtsp_url(self) -> str:
        """获取RTSP服务器地址
        Get RTSP server URL

        Returns:
            str: RTSP服务器地址 / RTSP server URL
        """
        return self.__rtst_url

    @property
    def width(self) -> int:
        """获取视频宽度
        Get video width

        Returns:
            int: 视频宽度(像素) / Video width(pixels)
        """
        return self.__width

    @width.setter
    def width(
        self, width: int
    ):  # 要设置的新视频宽度(像素) / New video width(pixels) to be set
        """设置视频宽度
        Set video width

        更新视频流的宽度参数，仅在推流未开始时有效
        Update the width parameter of video stream, only effective when streaming has not started

        Args:
            width (int): 视频宽度(像素)，必须为正整数 /
                Video width(pixels), must be a positive integer
        """
        if self.is_opened:
            return

        self.__width = width

        self.update_command()

    @property
    def height(self) -> int:
        """获取视频高度
        Get video height

        Returns:
            int: 视频高度(像素) / Video height(pixels)
        """
        return self.__height

    @height.setter
    def height(
        self, height: int
    ):  # 要设置的新视频高度(像素) / New video height(pixels) to be set
        """设置视频高度
        Set video height

        更新视频流的高度参数，仅在推流未开始时有效
        Update the height parameter of video stream, only effective when streaming has not started

        Args:
            height (int): 视频高度(像素)，必须为正整数 /
                Video height(pixels), must be a positive integer
        """
        if self.is_opened:
            return

        self.__height = height

        self.update_command()

    @property
    def fps(self) -> float:
        """获取视频帧率
        Get video frame rate

        Returns:
            float: 视频帧率，每秒传输的帧数 / Video frame rate, frames transmitted per second
        """
        return self.__fps

    @fps.setter
    def fps(self, fps: float):  # 要设置的新帧率 / New frame rate to be set
        """设置视频帧率
        Set video frame rate

        更新视频流的帧率参数，仅在推流未开始时有效
        Update the frame rate parameter of video stream, only effective when streaming has not started

        Args:
            fps (float): 帧率，每秒传输的帧数，必须为正数 / Frame rate, frames per second, must be positive
        """
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
        """设置NVIDIA GPU编码器参数
        Set NVIDIA GPU encoder parameters

        使用NVIDIA GPU硬件加速的H.264编码
        Use NVIDIA GPU hardware accelerated H.264 encoding
        """
        self.__params_encoder = [
            "-c:v",
            "h264_nvenc",
        ]

        self.update_command()

    def set_encoder_gpu_amd(self) -> None:
        """设置AMD GPU编码器参数
        Set AMD GPU encoder parameters

        使用AMD GPU硬件加速的H.264编码
        Use AMD GPU hardware accelerated H.264 encoding
        """
        self.__params_encoder = [
            "-c:v",
            "h264_amf",
        ]

        self.update_command()

    def update_command(self):
        """更新FFmpeg命令参数
        Update FFmpeg command parameters

        根据当前设置的宽度、高度、帧率和编码器构建FFmpeg命令行
        Build FFmpeg command line based on current width, height, frame rate and encoder settings
        """
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
        """打开RTSP推流
        Open RTSP streaming

        Returns:
            bool: 是否成功打开推流通道 / Whether streaming channel is successfully opened
        """
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
        """关闭RTSP推流
        Close RTSP streaming
        """
        if self.is_opened:
            try:
                self.__p.stdin.close()

                self.__open_have_error = False
                self.__opened = False
            except Exception as e:
                print(e)

    def __before_push(self) -> bool:
        """推流前的检查
        Checks before pushing stream

        确保推流已打开，如果未打开则尝试打开
        Ensure streaming is opened, try to open if not

        Returns:
            bool: 是否可以推流，推流通道是否准备就绪 /
                Whether can push stream, if streaming channel is ready
        """
        if not self.is_opened:
            # If last open not have error, try open again
            if not self.__open_have_error:
                if self.open():
                    return True

            return False

        return True

    def push_cv2(
        self, frame: np.ndarray
    ) -> (
        None
    ):  # OpenCV格式图像帧，BGR顺序的numpy数组 / OpenCV format image frame, numpy array in BGR order
        """推送OpenCV格式的帧
        Push frame in OpenCV format

        将OpenCV格式的图像帧(numpy数组)推送到RTSP流
        Push OpenCV format image frame(numpy array) to RTSP stream

        Args:
            frame (np.ndarray): OpenCV图像帧，BGR格式的numpy数组，形状应为(height, width, 3) /
                OpenCV image frame, numpy array in BGR format, shape should be (height, width, 3)
        """
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

    def push_pillow(self, image, convert_to_bgr: bool = True) -> None:
        """推送Pillow格式的图像
        Push image in Pillow format

        将Pillow库的图像对象转换并推送到RTSP流
        Convert and push Pillow library image object to RTSP stream

        Image为Pillow的Image对象，这里不要进行类型标注，因为用户可能使用的是OpenCV而没有安装Pillow。
        Image is Pillow's Image object, here don't annotate the type,
            because the user may use OpenCV without installing Pillow.

        Args:
            image (Image.Image): Pillow图像对象，通常为RGB格式(注意这里参数里面不要进行类型标注) /
                Pillow image object, usually in RGB format
            convert_to_bgr (bool, optional): 是否将RGB转换为OpenCV使用的BGR格式，默认为True /
                Whether to convert RGB to BGR format used by OpenCV, defaults to True
        """
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
        """安装ffmpeg
        Install ffmpeg

        在支持的系统上尝试安装ffmpeg
        Try to install ffmpeg on supported systems

        Returns:
            bool: 安装是否成功，ffmpeg是否可用 / Whether installation is successful, if ffmpeg is available
        """
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
        """检查是否为Linux系统
        Check if system is Linux

        Returns:
            bool: 是否为Linux系统 / Whether system is Linux
        """
        return platform.system() == "Linux"

    @staticmethod
    def is_windows() -> bool:
        """检查是否为Windows系统
        Check if system is Windows

        Returns:
            bool: 是否为Windows系统 / Whether system is Windows
        """
        return platform.system() == "Windows"

    @staticmethod
    def is_macos() -> bool:
        """检查是否为MacOS系统
        Check if system is MacOS

        Returns:
            bool: 是否为MacOS系统 / Whether system is MacOS
        """
        return platform.system() == "Darwin"

    def __del__(self):
        """析构函数，确保对象销毁时关闭推流
        Destructor, ensure streaming is closed when object is destroyed
        """
        self.close()

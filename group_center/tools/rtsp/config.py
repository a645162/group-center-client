import os


def get_rtsp_server() -> str:
    return os.getenv("RTSP_SERVER_URL", "")

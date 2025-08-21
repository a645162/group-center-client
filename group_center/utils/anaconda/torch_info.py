import os


def get_torch_info_utils_py_path():
    return os.path.abspath(__file__)


def is_torch_installed() -> bool:
    """
    检查是否已安装torch
    Returns True if torch is installed, False otherwise.
    """
    try:
        import torch  # noqa: F401

        return True
    except ImportError:
        return False


def is_cuda_available() -> bool:
    """
    判断当前PyTorch是否支持CUDA
    Returns True if CUDA is available.
    """
    import torch

    return torch.cuda.is_available()


def get_cuda_version() -> str:
    """
    获取支持的CUDA版本（如有）
    Returns the CUDA version supported by PyTorch, or empty string if not available.
    """
    import torch

    return torch.version.cuda if torch.version.cuda is not None else ""


def is_rocm_available() -> bool:
    """
    判断当前PyTorch是否为ROCm版本
    Returns True if ROCm is available.
    """
    import torch

    return hasattr(torch.version, "hip") and torch.version.hip is not None


def get_rocm_version() -> str:
    """
    获取支持的ROCm版本（如有）
    Returns the ROCm version supported by PyTorch, or empty string if not available.
    """
    import torch

    return (
        torch.version.hip
        if hasattr(torch.version, "hip") and torch.version.hip is not None
        else ""
    )


def is_intel_gpu_available() -> bool:
    """
    判断当前PyTorch是否为Intel GPU版本
    Returns True if Intel GPU (XPU) is available.
    """
    import torch

    return hasattr(torch, "xpu") and torch.xpu.is_available()


def get_intel_gpu_version() -> str:
    """
    获取支持的Intel GPU版本（如有）
    Returns the Intel GPU version supported by PyTorch, or empty string if not available.
    """
    import torch

    # Intel XPU通常没有单独的版本信息，返回torch版本或空字符串
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.__version__
    return ""


def get_torch_version() -> str:
    """
    获取当前PyTorch版本
    Returns the installed torch version.
    """
    import torch

    return torch.__version__


def get_available_devices() -> list:
    """
    获取可用的PyTorch设备类型列表
    Returns a list of available device types (e.g., ['cpu', 'cuda', 'xpu']).
    """
    devices = ["cpu"]
    try:
        import torch

        if torch.cuda.is_available():
            devices.append("cuda")
        if hasattr(torch, "xpu") and torch.xpu.is_available():
            devices.append("xpu")
        if hasattr(torch, "has_mps") and torch.has_mps:
            devices.append("mps")
    except Exception:
        pass
    return devices


def get_torch_compiler_info() -> str:
    """
    获取PyTorch编译器信息
    Returns PyTorch compiler version info.
    """
    try:
        import torch

        return torch.__config__.show().strip()
    except Exception:
        return ""


def get_blas_info() -> str:
    """
    获取PyTorch使用的BLAS库信息
    Returns BLAS info used by PyTorch.
    """
    try:
        import torch

        # 尝试多种方式获取BLAS信息
        if hasattr(torch._C, "_get_mkl_version"):
            return torch._C._get_mkl_version()
        elif hasattr(torch.version, "blas_info"):
            return str(torch.version.blas_info)
        else:
            # 从编译配置中提取BLAS信息
            config = torch.__config__.show()
            if "BLAS_INFO=" in config:
                for line in config.split("\n"):
                    if "BLAS_INFO=" in line:
                        return line.split("BLAS_INFO=")[1].split(",")[0]
        return "BLAS info not available"
    except Exception:
        return ""


def get_openmp_info() -> str:
    """
    获取OpenMP支持信息
    Returns OpenMP info used by PyTorch.
    """
    try:
        import torch

        # 从编译配置中获取OpenMP信息
        config = torch.__config__.show()
        if "OpenMP" in config:
            for line in config.split("\n"):
                if "OpenMP" in line and "a.k.a" in line:
                    # 去掉"- "前缀
                    text = line.strip()
                    if text.startswith("- "):
                        text = text[2:]
                    elif text.startswith("  - "):
                        text = text[4:]
                    return text
        return "OpenMP info not available"
    except Exception:
        return ""


def get_mkl_info() -> str:
    """
    获取MKL支持信息
    Returns MKL info used by PyTorch.
    """
    try:
        import torch

        # 从编译配置中获取MKL信息
        config = torch.__config__.show()
        if "Math Kernel Library" in config:
            for line in config.split("\n"):
                if "Math Kernel Library" in line:
                    # 去掉"- "前缀
                    text = line.strip()
                    if text.startswith("- "):
                        text = text[2:]
                    elif text.startswith("  - "):
                        text = text[4:]
                    return text
        return "MKL info not available"
    except Exception:
        return ""


def get_cudnn_version() -> str:
    """
    获取CuDNN版本信息
    Returns CuDNN version if available.
    """
    try:
        import torch

        if torch.cuda.is_available():
            version_int = torch.backends.cudnn.version()
            try:
                # 尝试将数字版本号转换为可读格式，如 8902 -> 8.9.2
                if version_int and version_int >= 1000:
                    major = version_int // 1000
                    minor = (version_int % 1000) // 100
                    patch = (version_int % 100) // 10
                    return f"{major}.{minor}.{patch}"
                else:
                    # 如果版本号格式不符合预期，返回原始值
                    return str(version_int)
            except Exception:
                # 如果格式化失败，回退到原始版本号
                return str(version_int)
        return ""
    except Exception:
        return ""


def get_cpu_info() -> str:
    """
    获取CPU优化信息
    Returns CPU optimization flags.
    """
    try:
        import torch

        # 从编译配置中获取CPU优化信息
        config = torch.__config__.show()
        cpu_info = []

        # 获取CPU能力信息
        if "CPU capability usage:" in config:
            for line in config.split("\n"):
                if "CPU capability usage:" in line:
                    # 去掉"- "前缀，然后取冒号后的内容
                    text = line.strip()
                    if text.startswith("- "):
                        text = text[2:]
                    elif text.startswith("  - "):
                        text = text[4:]

                    if ":" in text:
                        text = text.split(":", 1)[1].strip()

                    cpu_info.append(f"CPU capability: {text}")

        # 检查性能优化标志，避免重复
        avx_flags = []
        if "PERF_WITH_AVX=" in config:
            for line in config.split("\n"):
                if "PERF_WITH_AVX=" in line:
                    parts = line.split("PERF_WITH_AVX=")[1].split(",")[0]
                    if "1" in parts:
                        avx_flags.append("AVX")

        if "PERF_WITH_AVX2=" in config:
            for line in config.split("\n"):
                if "PERF_WITH_AVX2=" in line:
                    parts = line.split("PERF_WITH_AVX2=")[1].split(",")[0]
                    if "1" in parts and "AVX2" not in str(cpu_info):
                        avx_flags.append("AVX2")

        if "PERF_WITH_AVX512=" in config:
            for line in config.split("\n"):
                if "PERF_WITH_AVX512=" in line:
                    parts = line.split("PERF_WITH_AVX512=")[1].split(",")[0]
                    if "1" in parts:
                        avx_flags.append("AVX512")

        if avx_flags:
            cpu_info.append(f"Performance optimizations: {', '.join(avx_flags)}")

        return (
            "; ".join(cpu_info) if cpu_info else "CPU optimization info not available"
        )
    except Exception:
        return ""


def get_nvcc_flags() -> str:
    """
    获取NVCC架构标志
    Returns NVCC architecture flags.
    """
    try:
        import torch

        config = torch.__config__.show()
        if "NVCC architecture flags:" in config:
            for line in config.split("\n"):
                if "NVCC architecture flags:" in line:
                    # 去掉"- "前缀，然后取冒号后的内容
                    text = line.strip()
                    if text.startswith("- "):
                        text = text[2:]
                    elif text.startswith("  - "):
                        text = text[4:]

                    if ":" in text:
                        text = text.split(":", 1)[1].strip()

                    # 提取sm_开头的架构代码
                    sm_codes = []
                    parts = text.split(";")
                    for part in parts:
                        if "code=sm_" in part:
                            sm_code = part.split("code=sm_")[1]
                            if sm_code:
                                sm_codes.append(f"sm_{sm_code}")

                    return ", ".join(sm_codes) if sm_codes else text
        return "NVCC flags not available"
    except Exception:
        return ""


def main():
    print("Torch Info Utils:", get_torch_info_utils_py_path())

    print(f"Torch 是否已安装: {is_torch_installed()}")

    if is_torch_installed():
        print(f"Torch 版本: {get_torch_version()}")
        print(f"可用设备: {get_available_devices()}")
        print(f"CUDA 是否可用: {is_cuda_available()}")

        # 示例：调用 get_cuda_version 函数以获取支持的 CUDA 版本
        # 你可以通过以下方式直接调用此函数：
        # python -c "from group_center.utils.anaconda.torch_info import get_cuda_version; print(get_cuda_version())"

        print(f"CUDA 版本: {get_cuda_version()}")
        print(f"CuDNN 版本: {get_cudnn_version()}")
        print(f"NVCC 标志: {get_nvcc_flags()}")
        print(f"ROCm 是否可用: {is_rocm_available()}")
        print(f"ROCm 版本: {get_rocm_version()}")
        print(f"Intel GPU 是否可用: {is_intel_gpu_available()}")
        print(f"Intel GPU 版本: {get_intel_gpu_version()}")
        print(f"CPU 优化: {get_cpu_info()}")
        print("BLAS 信息:", get_blas_info())
        print("OpenMP 信息:", get_openmp_info())
        print("MKL 信息:", get_mkl_info())
        print("PyTorch 编译信息:")
        print(get_torch_compiler_info())
    else:
        print("Torch 未安装，无法获取相关信息")


if __name__ == "__main__":
    main()

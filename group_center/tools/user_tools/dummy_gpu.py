try:
    import torch
except ImportError:
    print("Torch is not installed. Please install it to use this script.")
    exit(1)
import time
import argparse


def run_dummy_gpu(size_mb: int):
    # 检查CUDA是否可用
    if not torch.cuda.is_available():
        print("CUDA不可用，使用CPU模式")
        device = torch.device("cpu")
    else:
        device = torch.device("cuda:0")
        print(f"使用GPU: {torch.cuda.get_device_name(0)}")

    # 计算需要的张量大小来占用指定显存
    # MB -> bytes, float32 = 4 bytes
    size = int(size_mb * 1024 * 1024 / 4)

    try:
        dummy_tensor = torch.randn(size, device=device, dtype=torch.float32)
        print(f"成功分配约{size_mb}MB显存")
        if device.type == "cuda":
            print(f"当前显存使用: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
            print(f"显存缓存: {torch.cuda.memory_reserved(0) / 1024**2:.2f} MB")

        print("进程将保持运行，按Ctrl+C退出...")

        while True:
            time.sleep(60)
            if device.type == "cuda":
                print(
                    f"显存使用状态: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB"
                )
            else:
                print("进程正在运行中...")

    except RuntimeError as e:
        print(f"显存分配失败: {e}")
        print("尝试分配较小的显存...")
        size = size // 2
        dummy_tensor = torch.randn(size, device=device, dtype=torch.float32)
        print(f"分配了约{size * 4 / 1024**2:.2f}MB显存")

        while True:
            time.sleep(60)
            if device.type == "cuda":
                print(
                    f"显存使用状态: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB"
                )
            else:
                print("进程正在运行中...")

    except KeyboardInterrupt:
        print("\n收到退出信号，清理显存...")

        # Release GPU memory
        del dummy_tensor

        if device.type == "cuda":
            torch.cuda.empty_cache()
        print("进程已退出")


def main():
    parser = argparse.ArgumentParser(description="占用指定显存的dummy GPU进程")
    parser.add_argument(
        "--size",
        type=int,
        default=1024,
        help="分配显存大小（MB），默认1024MB",
    )
    args = parser.parse_args()
    run_dummy_gpu(args.size)


if __name__ == "__main__":
    main()

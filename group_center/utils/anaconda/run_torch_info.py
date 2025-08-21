import subprocess
import sys
import os
from typing import Optional

from group_center.utils.anaconda.torch_info import get_torch_info_utils_py_path


def run_torch_info(python_interpreter: str, function_name: str) -> Optional[str]:
    """
    使用指定的Python解释器运行torch_info中的函数并返回输出字符串
    Run the specified function using the given Python interpreter and return its output as a string.

    Args:
        python_interpreter (str): Python解释器的路径 | Path to the Python interpreter.
        function_name (str): 要调用的函数名 | Name of the function to call.

    Returns:
        Optional[str]: 函数输出的字符串 | Output of the function as a string, or None if failed.
    """
    try:
        # 获取torch_info.py的绝对路径

        torch_info_path = get_torch_info_utils_py_path()
        current_dir = os.path.dirname(torch_info_path)

        if not os.path.exists(torch_info_path):
            raise FileNotFoundError(f"torch_info.py not found at: {torch_info_path}")

        # print(f"Using torch_info.py at: {torch_info_path}")

        # 使用指定的Python解释器直接执行文件中的函数
        result = subprocess.run(
            [
                python_interpreter,
                "-c",
                f"import sys; sys.path.insert(0, '{current_dir}'); "
                f"from torch_info import {function_name}; print({function_name}())",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise RuntimeError(f"Error executing function: {result.stderr.strip()}")

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # 获取当前Python解释器路径进行测试
    current_python = sys.executable
    print(f"当前Python解释器路径: {current_python}")

    func_name = "get_cuda_version"
    output = run_torch_info(current_python, func_name)
    if output is not None:
        print(f"Output of '{func_name}': {output}")
    else:
        print(f"Failed to execute '{func_name}'.")

    # 测试其他函数
    test_functions = ["get_torch_version", "is_cuda_available", "get_available_devices"]
    for func in test_functions:
        result = run_torch_info(current_python, func)
        print(f"{func}: {result}")
    if output is not None:
        print(f"Output of '{func_name}': {output}")
    else:
        print(f"Failed to execute '{func_name}'.")

    # 测试其他函数
    test_functions = ["get_torch_version", "is_cuda_available", "get_available_devices"]
    for func in test_functions:
        result = run_torch_info(current_python, func)
        print(f"{func}: {result}")

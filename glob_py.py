import os
import glob
from typing import List
import argparse  # 用于命令行参数解析 for command-line argument parsing

import tqdm

prompt = """
任务：
请你为下面的py文件添加注释与数据类型标注，要求同时包含中文注释和英文注释。

要求：
如果已经存在中文注释，就不要修改现有的中文注释，直接添加英文注释！
（中文注释在前面）
不要修改任何代码逻辑！

中途不要咨询我任何意见，你自己决定，处理所有文件！
中途不需要确认，现在就开始执行！
双语注释在同一行！一个参数你两行，vscoded调用函数的时候，显示注释就会不全！很奇怪！

文件列表：
"""


def traverse_files(extension: str = "py") -> List[str]:
    """遍历指定扩展名的文件
    Traverse files with specified extension

    Args:
        extension (str): 文件扩展名 | File extension

    Returns:
        List[str]: 匹配的文件路径列表 | List of matched file paths
    """
    pattern = f"**/*.{extension}"  # 构造匹配模式 构建 pattern string
    files = glob.glob(pattern, recursive=True)  # 遍历所有子目录 Traverse subdirectories
    return files


def convert_to_cline_list(files: List[str]) -> List[str]:
    """将文件路径转换为Cline格式
    Convert file paths to Cline format

    Args:
        files (List[str]): 文件路径列表 | List of file paths

    Returns:
        List[str]: 转换后的文件路径列表 | Converted file paths list
    """
    return [f"@/{file}" for file in files]


def batch_files(files: List[str], batch_size: int) -> List[List[str]]:
    """
    将文件列表按 batch_size 切分
    Split the file list into batches with batch_size

    Args:
        files (List[str]): 文件路径列表 | List of file paths
        batch_size (int): 每批文件数量 | Number of files per batch

    Returns:
        List[List[str]]: 分批次的文件路径列表 | Batched file paths list
    """
    if batch_size <= 0:
        return [files]
    return [files[i : i + batch_size] for i in range(0, len(files), batch_size)]


if __name__ == "__main__":
    # 获取当前脚本目录 Get current script directory
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)  # 切换到脚本目录 Change working directory

    # 解析命令行参数 Parse command-line arguments
    parser = argparse.ArgumentParser(description="Batch processing of Python files")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="批处理大小（小于等于0表示所有文件为一个 batch） | Batch size (<=0 means one batch)",
    )
    args = parser.parse_args()

    files: List[str] = traverse_files()
    files: List[str] = convert_to_cline_list(files)

    # Sort
    files.sort()

    batches: List[List[str]] = batch_files(files, args.batch_size)

    output_dir_path = "tmp"
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    file_name_template = "batch_{}.txt"

    # 逐个 batch 输出 Print each batch
    for index, batch in tqdm.tqdm(enumerate(batches, start=1)):
        batch_str = " 和 ".join(batch)

        text = prompt.strip() + "\n" + batch_str

        file_path = os.path.join(output_dir_path, file_name_template.format(index))
        with open(file_path, "w") as f:
            f.write(text)
            f.write("\n")

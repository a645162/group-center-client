import os
import shutil
import fnmatch
import argparse
import sys
from typing import List, Tuple

# Python缓存目录列表 / Python cache directory list
# 这些目录通常包含临时文件和缓存，可以安全删除
# These directories typically contain temporary files and caches that can be safely removed
PYTHON_CACHE_DIRS: List[str] = [
    "__pycache__",  # Python 3的字节码缓存目录 / Python 3 bytecode cache directory
    ".pytest_cache",  # PyTest测试框架的缓存目录 / PyTest framework cache directory
    ".coverage",  # 代码覆盖率工具的缓存目录 / Code coverage tool cache directory
    ".mypy_cache",  # MyPy类型检查的缓存目录 / MyPy type checking cache directory
    ".tox",  # Tox测试工具的缓存目录 / Tox testing tool cache directory
    ".eggs",  # Python包构建的临时目录 / Python package build temporary directory
    "*.egg-info",  # Python包元数据目录 / Python package metadata directory
    "build",  # 构建输出目录 / Build output directory
    "dist",  # 分发包目录 / Distribution package directory
    ".ipynb_checkpoints",  # Jupyter notebook的检查点目录 / Jupyter notebook checkpoints
]

# Python缓存文件列表 / Python cache file list
# 这些文件通常是自动生成的，可以安全删除
# These files are typically auto-generated and can be safely removed
PYTHON_CACHE_FILES: List[str] = [
    "*.pyc",  # 编译的Python字节码文件 / Compiled Python bytecode files
    "*.pyo",  # 优化的Python字节码文件 / Optimized Python bytecode files
    "*.pyd",  # Python扩展模块 / Python extension modules
    "*.so",  # 共享对象库文件 / Shared object library files
    "*.dll",  # 动态链接库文件 / Dynamic link library files
    "*.exe",  # 可执行文件 / Executable files
    ".coverage",  # 代码覆盖率数据文件 / Code coverage data file
    "coverage.xml",  # XML格式的覆盖率报告 / XML format coverage report
    ".DS_Store",  # macOS目录元数据文件 / macOS directory metadata file
    "*.log",  # 日志文件 / Log files
]


def safe_remove_file(file_path: str) -> bool:
    """
    安全地删除文件，处理可能的异常
    Safely remove a file while handling possible exceptions

    Args:
        file_path (str): 要删除的文件路径 / Path to the file to be removed

    Returns:
        bool: 删除成功返回True，失败返回False / Returns True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            print(f"Removing cache file: {file_path}")
            os.remove(file_path)
            return True
    except (OSError, PermissionError) as e:
        # 处理权限错误或其他IO错误 / Handle permission errors or other IO errors
        print(f"Failed to remove file {file_path}: {e}")
    return False


def safe_remove_dir(dir_path: str) -> bool:
    """
    安全地删除目录，处理可能的异常
    Safely remove a directory while handling possible exceptions

    Args:
        dir_path (str): 要删除的目录路径 / Path to the directory to be removed

    Returns:
        bool: 删除成功返回True，失败返回False / Returns True if successful, False otherwise
    """
    try:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"Removing cache directory: {dir_path}")
            shutil.rmtree(dir_path)
            return True
    except (OSError, PermissionError) as e:
        # 处理权限错误或其他IO错误 / Handle permission errors or other IO errors
        print(f"Failed to remove directory {dir_path}: {e}")
    return False


def remove_python_temp_files(path: str) -> None:
    """
    递归删除指定路径下的Python临时文件
    Recursively remove Python temporary files from the specified path

    Args:
        path (str): 起始路径 / Starting path for cleanup
    """
    try:
        for root, dirs, files in os.walk(path):
            # 处理Python缓存目录 / Handle Python cache directories
            dirs_to_remove = []
            for dir_name in dirs:
                if _should_remove_dir(dir_name):
                    cache_path = os.path.join(root, dir_name)
                    if safe_remove_dir(cache_path):
                        # 记录成功删除的目录 / Record successfully removed directories
                        dirs_to_remove.append(dir_name)

            # 从dirs列表中移除已删除的目录，防止os.walk继续遍历它们
            # Remove deleted directories from dirs list to prevent os.walk from traversing them
            for dir_name in dirs_to_remove:
                if dir_name in dirs:
                    dirs.remove(dir_name)

            # 处理Python缓存文件 / Handle Python cache files
            for file_name in files:
                if _should_remove_file(file_name):
                    file_path = os.path.join(root, file_name)
                    safe_remove_file(file_path)
    except Exception as e:
        # 捕获任何未预见的异常 / Catch any unforeseen exceptions
        print(f"Error occurred while removing temp files: {e}")


def _should_remove_dir(dir_name: str) -> bool:
    """
    检查目录是否应该被删除
    Check if a directory should be removed

    Args:
        dir_name (str): 要检查的目录名 / Directory name to check

    Returns:
        bool: 如果目录应该被删除则返回True / Returns True if directory should be removed
    """
    for pattern in PYTHON_CACHE_DIRS:
        if pattern.endswith("*"):
            # 处理通配符模式 / Handle wildcard patterns
            if fnmatch.fnmatch(dir_name, pattern):
                return True
        elif dir_name == pattern:
            # 精确匹配 / Exact match
            return True
    return False


def _should_remove_file(file_name: str) -> bool:
    """
    检查文件是否应该被删除
    Check if a file should be removed

    Args:
        file_name (str): 要检查的文件名 / File name to check

    Returns:
        bool: 如果文件应该被删除则返回True / Returns True if file should be removed
    """
    for pattern in PYTHON_CACHE_FILES:
        # 使用fnmatch进行通配符匹配 / Use fnmatch for wildcard matching
        if fnmatch.fnmatch(file_name, pattern):
            return True
    return False


def remove_empty_dirs(path: str) -> None:
    """
    递归删除指定路径下的空目录
    Recursively remove empty directories from the specified path

    Args:
        path (str): 起始路径 / Starting path for cleanup
    """
    try:
        # 自底向上遍历目录（topdown=False）以确保先处理子目录
        # Traverse directories bottom-up (topdown=False) to ensure child directories are processed first
        for root, dirs, _ in os.walk(path, topdown=False):
            for dir_name in dirs:
                _check_and_remove_empty_dir(os.path.join(root, dir_name), path)
    except Exception as e:
        # 捕获任何未预见的异常 / Catch any unforeseen exceptions
        print(f"Error occurred while removing empty directories: {e}")


def _check_and_remove_empty_dir(dir_path: str, base_path: str) -> None:
    """
    检查并删除空目录，以及可能变空的父目录
    Check and remove empty directories, and possibly emptied parent directories

    Args:
        dir_path (str): 要检查的目录路径 / Path to directory to check
        base_path (str): 基础路径，避免删除基础路径之上的目录 / Base path to avoid removing directories above it
    """
    try:
        # 检查路径是否有效 / Check if path is valid
        if not os.path.isdir(dir_path) or not os.path.exists(dir_path):
            return

        # 检查目录是否为空 / Check if directory is empty
        if not os.listdir(dir_path):
            print(f"Removing empty directory: {dir_path}")
            os.rmdir(dir_path)

            # 检查父目录是否变为空 / Check if parent directory became empty
            parent_dir = os.path.dirname(dir_path)
            # 如果父目录不是基础路径且存在，则递归检查 / If parent is not base path and exists, check recursively
            if parent_dir != base_path and os.path.exists(parent_dir):
                _check_and_remove_empty_dir(parent_dir, base_path)
    except (OSError, PermissionError) as e:
        # 处理权限错误或其他IO错误 / Handle permission errors or other IO errors
        print(f"Failed to check/remove directory {dir_path}: {e}")


def count_removable_items(path: str) -> Tuple[int, int]:
    """
    统计可删除的文件和目录数量
    Count the number of removable files and directories

    Args:
        path (str): 起始路径 / Starting path for counting

    Returns:
        tuple: (文件数量, 目录数量) / (file count, directory count)
    """
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(path):
        # 计算可删除的目录
        for dir_name in dirs:
            if _should_remove_dir(dir_name):
                dir_count += 1

        # 计算可删除的文件
        for file_name in files:
            if _should_remove_file(file_name):
                file_count += 1

    return file_count, dir_count


def preview_removable_items(path: str, max_items: int = 20) -> None:
    """
    预览将被删除的文件和目录
    Preview files and directories that will be removed

    Args:
        path (str): 起始路径 / Starting path for preview
        max_items (int): 最大显示数量 / Maximum number of items to display
    """
    items_to_remove = []

    for root, dirs, files in os.walk(path):
        # 预览可删除的目录
        for dir_name in dirs:
            if _should_remove_dir(dir_name):
                items_to_remove.append(f"目录/Dir: {os.path.join(root, dir_name)}")

        # 预览可删除的文件
        for file_name in files:
            if _should_remove_file(file_name):
                items_to_remove.append(f"文件/File: {os.path.join(root, file_name)}")

        if len(items_to_remove) >= max_items:
            break

    # 显示预览项目
    for item in items_to_remove[:max_items]:
        print(item)

    if len(items_to_remove) > max_items:
        print("... 还有更多项目 / ... and more items")


def main() -> None:
    try:
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Python项目缓存清理工具 / Python project cache cleanup tool"
        )
        parser.add_argument(
            "--path",
            "-p",
            default=".",
            help="要清理的目录路径 / Path to clean (default: current directory)",
        )
        parser.add_argument(
            "--preview",
            "-v",
            action="store_true",
            help="仅预览将被删除的项目 / Only preview items to be removed",
        )
        parser.add_argument(
            "--yes",
            "-y",
            action="store_true",
            help="无需确认直接删除 / Delete without confirmation",
        )

        args: argparse.Namespace = parser.parse_args()
        target_path: str = os.path.abspath(args.path)

        # 验证路径存在
        if not os.path.exists(target_path):
            print(f"错误：路径不存在 / Error: Path does not exist: {target_path}")
            sys.exit(1)

        # 显示目标路径
        print(f"目标路径 / Target path: {target_path}")

        # 计算将被删除的项目
        file_count: int
        dir_count: int
        file_count, dir_count = count_removable_items(target_path)
        print(f"发现 {file_count} 个缓存文件和 {dir_count} 个缓存目录可被清理")
        print(
            f"Found {file_count} cache files and {dir_count} cache directories that can be cleaned"
        )

        # 预览模式
        if args.preview:
            print("\n预览将被删除的项目 / Preview of items to be removed:")
            preview_removable_items(target_path)
            print(
                "\n这是预览模式，未执行任何删除操作 / This is preview mode, no deletion performed"
            )
            sys.exit(0)

        # 确认删除
        if not args.yes:
            confirm: str = input(
                "\n确认清理这些文件？(y/n): / Confirm cleaning these files? (y/n): "
            )
            if confirm.lower() not in ["y", "yes"]:
                print("操作已取消 / Operation cancelled")
                sys.exit(0)

        # 执行清理
        print("开始Python缓存清理... / Starting Python cache cleanup...")
        remove_python_temp_files(target_path)
        print("开始空目录清理... / Starting empty directory cleanup...")
        remove_empty_dirs(target_path)
        print("清理完成。/ Cleanup completed.")
    except Exception as e:
        # 捕获主程序中的任何异常 / Catch any exceptions in the main program
        print(f"发生意外错误 / An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

import subprocess
import csv
import os
import json
import multiprocessing
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

from group_center.utils.anaconda.run_torch_info import run_torch_info


def get_conda_environments() -> List[Dict[str, str]]:
    """
    获取所有conda环境及其Python可执行路径
    Get all conda environments and their Python executable paths

    Returns:
        List[Dict[str, str]]: 环境信息列表 | List of environment information
    """
    try:
        # 使用conda info --envs --json获取环境信息
        result = subprocess.run(
            ["conda", "info", "--envs", "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            print(f"Error getting conda environments: {result.stderr}")
            return []

        envs_info = json.loads(result.stdout)
        environments = []

        for env_path in envs_info.get("envs", []):
            env_name = os.path.basename(env_path)
            if env_name == "envs":  # Skip the envs directory itself
                continue

            # 构建Python可执行文件路径
            if os.name == "nt":  # Windows
                python_path = os.path.join(env_path, "python.exe")
            else:  # Unix/Linux/macOS
                python_path = os.path.join(env_path, "bin", "python")

            # 检查Python可执行文件是否存在
            if os.path.exists(python_path):
                environments.append(
                    {
                        "name": env_name,
                        "path": env_path,
                        "python_executable": python_path,
                    }
                )

        return environments

    except Exception as e:
        print(f"Error: {e}")
        return []


def get_torch_info_for_env(python_executable: str) -> Dict[str, str]:
    """
    获取指定环境的torch相关信息
    Get torch information for the specified environment

    Args:
        python_executable (str): Python可执行文件路径 | Path to Python executable

    Returns:
        Dict[str, str]: torch信息字典 | Dictionary containing torch information
    """
    info = {
        "torch_version": "N/A",
        "cuda_version": "N/A",
    }

    try:
        # 获取torch版本
        torch_version = run_torch_info(python_executable, "get_torch_version")
        if torch_version:
            info["torch_version"] = torch_version

        # 获取CUDA版本
        cuda_version = run_torch_info(python_executable, "get_cuda_version")
        if cuda_version:
            info["cuda_version"] = cuda_version

    except Exception as e:
        print(f"Error getting torch info for {python_executable}: {e}")

    return info


def export_to_csv(
    environments_info: List[Dict], output_path: str = "conda_torch_info.csv"
):
    """
    将环境信息导出到CSV文件
    Export environment information to CSV file

    Args:
        environments_info (List[Dict]): 环境信息列表 | List of environment information
        output_path (str): 输出CSV文件路径 | Output CSV file path
    """
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            # 把 user 提到最前面
            fieldnames = [
                "user",
                "environment_name",
                "environment_path",
                "python_executable",
                "torch_version",
                "cuda_version",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for env_info in environments_info:
                # 只写入指定字段，额外字段将被忽略
                writer.writerow({k: env_info.get(k, "") for k in fieldnames})

        print(f"Results exported to: {output_path}")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")


def process_single_environment(env: Dict[str, str]) -> Dict[str, str]:
    """
    处理单个环境的torch信息获取
    Process torch information for a single environment

    Args:
        env (Dict[str, str]): 环境信息 | Environment information

    Returns:
        Dict[str, str]: 完整的环境信息 | Complete environment information
    """
    print(f"正在处理环境: {env['name']}")
    print(f"Python路径: {env['python_executable']}")

    # 获取torch信息
    torch_info = get_torch_info_for_env(env["python_executable"])

    # 根据路径提取用户名（如果以 /home/ 开头）
    user = ""
    try:
        env_path_norm = os.path.normpath(env["path"])
        # 确保以 /home/<username>/... 形式
        if env_path_norm.startswith(
            os.path.join(os.sep, "home", "")
        ) or env_path_norm.startswith("/home/"):
            parts = env_path_norm.split(os.sep)
            # parts example: ['', 'home', 'username', ...]
            if len(parts) >= 3 and parts[1] == "home":
                user = parts[2]
    except Exception:
        user = ""

    # 合并环境信息和torch信息，去掉 cuda_available 和 available_devices
    env_complete_info = {
        "environment_name": env["name"],
        "environment_path": env["path"],
        "python_executable": env["python_executable"],
        "user": user,
        **torch_info,
    }

    # 打印当前环境的信息（不再打印已移除的字段）
    print(f"  [{env['name']}] Torch版本: {torch_info.get('torch_version', 'N/A')}")
    print(f"  [{env['name']}] CUDA版本: {torch_info.get('cuda_version', 'N/A')}")
    if user:
        print(f"  [{env['name']}] 用户: {user}")

    return env_complete_info


def main():
    """
    主函数：列出所有conda环境，并行获取torch信息，并导出到CSV
    Main function: List all conda environments, get torch info in parallel, and export to CSV
    """
    print("正在获取conda环境列表...")
    environments = get_conda_environments()

    if not environments:
        print("未找到conda环境")
        return

    print(f"找到 {len(environments)} 个conda环境")

    # 计算线程池大小（CPU核心数的一半）
    max_workers = max(1, multiprocessing.cpu_count() // 2)
    print(f"使用 {max_workers} 个线程并行处理...")

    # 收集所有环境的信息
    all_env_info = []

    # 使用线程池并行处理环境
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_env = {
            executor.submit(process_single_environment, env): env
            for env in environments
        }

        # 处理完成的任务
        completed_count = 0
        for future in as_completed(future_to_env):
            env = future_to_env[future]
            try:
                env_complete_info = future.result()
                all_env_info.append(env_complete_info)
                completed_count += 1
                print(f"进度: {completed_count}/{len(environments)} 完成")
            except Exception as exc:
                print(f"环境 {env['name']} 处理失败: {exc}")

    # 根据原始脚本文件名生成输出文件名：原始文件名_YYYYMMDD_HHMMSS.csv
    original_name = "conda_torch_environments"

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{original_name}_{timestamp}.csv"

    export_to_csv(all_env_info, output_file)

    print(f"\n完成！结果已保存到: {output_file}")


if __name__ == "__main__":
    main()

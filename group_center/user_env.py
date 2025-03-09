from group_center.tools.user_env import *

if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()

    table = Table(title="环境信息概览", box=box.ROUNDED)
    table.add_column("类别", justify="left", style="cyan")
    table.add_column("值", justify="left", style="green")

    table.add_row("Python 版本", PythonVersion)
    table.add_row("Conda 环境", CONDA_ENV_NAME())
    table.add_row("CUDA 版本", CUDA_VERSION() or "未找到")
    table.add_row("Screen 会话", ENV_SCREEN_SESSION_NAME() or "无")

    console.print(table)

    console.print("\n[bold]详细环境信息:[/bold]")
    console.print(f"[cyan]Screen 全名:[/cyan] {ENV_SCREEN_NAME_FULL()}")
    console.print(f"[cyan]Screen ID:[/cyan] {ENV_SCREEN_SESSION_ID()}")
    console.print(f"[cyan]CUDA 根目录:[/cyan] {ENV_CUDA_ROOT() or '未找到'}")
    console.print(f"[cyan]CUDA 本地 Rank:[/cyan] {ENV_CUDA_LOCAL_RANK() or '未设置'}")
    console.print(f"[cyan]CUDA World Size:[/cyan] {ENV_CUDA_WORLD_SIZE() or '未设置'}")
    console.print(f"[cyan]运行命令:[/cyan] {RUN_COMMAND()}")

from group_center.tools.user_env import (
    PythonVersion,
    CONDA_ENV_NAME,
    CUDA_VERSION,
    ENV_SCREEN_SESSION_NAME,
    ENV_SCREEN_NAME_FULL,
    ENV_SCREEN_SESSION_ID,
    ENV_CUDA_ROOT,
    ENV_CUDA_LOCAL_RANK,
    ENV_CUDA_WORLD_SIZE,
    RUN_COMMAND,
)  # 导入用户环境工具 / Import user environment tools

if __name__ == "__main__":
    from rich.console import Console  # 控制台输出 / Console output
    from rich.table import Table  # 表格显示 / Table display
    from rich import box  # 表格边框样式 / Table border style

    console: Console = Console()  # 初始化控制台 / Initialize console

    # 创建环境信息表格 / Create environment info table
    table: Table = Table(title="环境信息概览 | Environment Overview", box=box.ROUNDED)
    table.add_column("类别 | Category", justify="left", style="cyan")
    table.add_column("值 | Value", justify="left", style="green")

    # 添加环境信息行 / Add environment info rows
    table.add_row("Python 版本 | Python Version", PythonVersion)
    table.add_row("Conda 环境 | Conda Environment", CONDA_ENV_NAME())
    table.add_row("CUDA 版本 | CUDA Version", CUDA_VERSION() or "未找到 | Not found")
    table.add_row(
        "Screen 会话 | Screen Session", ENV_SCREEN_SESSION_NAME() or "无 | None"
    )

    console.print(table)  # 打印表格 / Print table

    # 打印详细环境信息 / Print detailed environment info
    console.print("\n[bold]详细环境信息 | Detailed Environment Info:[/bold]")
    console.print(
        f"[cyan]Screen 全名 | Screen Full Name:[/cyan] {ENV_SCREEN_NAME_FULL()}"
    )
    console.print(f"[cyan]Screen ID:[/cyan] {ENV_SCREEN_SESSION_ID()}")
    console.print(
        f"[cyan]CUDA 根目录 | CUDA Root:[/cyan] {ENV_CUDA_ROOT() or '未找到 | Not found'}"
    )
    console.print(
        f"[cyan]CUDA 本地 Rank | CUDA Local Rank:[/cyan] {ENV_CUDA_LOCAL_RANK() or '未设置 | Not set'}"
    )
    console.print(
        f"[cyan]CUDA World Size:[/cyan] {ENV_CUDA_WORLD_SIZE() or '未设置 | Not set'}"
    )
    console.print(f"[cyan]运行命令 | Run Command:[/cyan] {RUN_COMMAND()}")

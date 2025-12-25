#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conda环境清理工具 / Conda Environment Cleanup Tool

提供交互式界面用于选择并删除conda环境
Provides an interactive interface for selecting and deleting conda environments
"""

import subprocess
import sys
import argparse
from typing import List, Tuple

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("警告：未找到rich库，将使用基本命令行界面 / Warning: rich library not found, using basic CLI")
    # 定义替代函数 / Define alternative functions
    class Console:
        def __init__(self): pass
        def print(self, *args, **kwargs): print(*args, **kwargs)
    class Prompt:
        @staticmethod
        def ask(*args, **kwargs):
            if args:
                return input(args[0] + " ")
            return input("请输入: ")
    class Confirm:
        @staticmethod
        def ask(*args, **kwargs):
            if args:
                response = input(args[0] + " (y/n): ").lower()
            else:
                response = input("确认？ (y/n): ").lower()
            return response in ['y', 'yes']
    # 定义Table类作为占位符 / Define Table class as placeholder
    class Table:
        def __init__(self, *args, **kwargs): pass
        def add_column(self, *args, **kwargs): pass
        def add_row(self, *args, **kwargs): pass


class CondaEnv:
    """Conda环境信息 / Conda environment information"""
    
    def __init__(self, name: str, path: str, is_active: bool = False, selected: bool = False):
        self.name = name
        self.path = path
        self.is_active = is_active
        self.selected = selected
    
    def __repr__(self) -> str:
        return f"CondaEnv(name={self.name}, path={self.path}, is_active={self.is_active})"


def get_conda_envs() -> List[CondaEnv]:
    """
    获取所有conda环境列表 / Get list of all conda environments
    
    Returns:
        List[CondaEnv]: Conda环境对象列表 / List of Conda environment objects
    """
    try:
        # 执行conda env list命令 / Execute conda env list command
        # 使用兼容Python 3.6的方式 / Use Python 3.6 compatible way
        result = subprocess.run(
            ["conda", "env", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # 在Python 3.6中相当于text=True / Equivalent to text=True in Python 3.6
            check=True
        )
        
        envs = []
        lines = result.stdout.strip().split('\n')
        
        # 解析输出，跳过标题行 / Parse output, skip header lines
        for line in lines:
            line = line.strip()
            # 跳过空行和注释行 / Skip empty lines and comment lines
            if not line or line.startswith('#') or '#' in line and line.split('#')[0].strip() == '':
                continue
            
            # 解析环境名称和路径 / Parse environment name and path
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                path = parts[-1]
                
                # 检查是否为当前活动环境 / Check if this is the current active environment
                is_active = False
                if name == '*':
                    # 如果第一列是*，那么环境名在第二列 / If first column is *, environment name is in second column
                    if len(parts) >= 3:
                        name = parts[1]
                        is_active = True
                    else:
                        continue
                
                # 跳过base环境（通常不建议删除） / Skip base environment (usually not recommended to delete)
                if name.lower() == 'base':
                    continue
                    
                envs.append(CondaEnv(name=name, path=path, is_active=is_active))
        
        return envs
        
    except subprocess.CalledProcessError as e:
        print("错误：无法获取conda环境列表 / Error: Failed to get conda environment list")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("错误：未找到conda命令。请确保conda已安装并在PATH中 / Error: conda command not found. Make sure conda is installed and in PATH")
        sys.exit(1)


def print_env_list(envs: List[CondaEnv]) -> None:
    """
    打印环境列表 / Print environment list
    
    Args:
        envs: Conda环境列表 / List of Conda environments
    """
    if not envs:
        print("未找到conda环境 / No conda environments found")
        return
    
    print("\nConda环境列表 / Conda Environment List:")
    print("=" * 80)
    print(f"{'序号':<6} {'环境名称':<20} {'路径':<40} {'状态':<10}")
    print("-" * 80)
    
    for i, env in enumerate(envs, 1):
        status = "活跃/Active" if env.is_active else "未激活/Inactive"
        print(f"{i:<6} {env.name:<20} {env.path[:38]:<40} {status:<10}")
    
    print("=" * 80)


def interactive_select_envs(envs: List[CondaEnv]) -> Tuple[List[CondaEnv], bool]:
    """
    交互式选择环境 / Interactive environment selection
    
    Args:
        envs: Conda环境列表 / List of Conda environments
        
    Returns:
        Tuple[List[CondaEnv], bool]: (用户选择的环境列表, 是否执行conda clean) /
        (List of environments selected by user, whether to run conda clean)
    """
    # 尝试使用curses实现真正的交互式界面 / Try to use curses for real interactive interface
    try:
        import curses
        import curses.ascii
        
        def draw_menu(stdscr, selected_idx: int, selected_indices: set, run_clean: bool):
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # 标题 / Title
            title = "Conda环境清理工具 - 交互式选择 (上下键移动, 空格选择, Enter确认)"
            title_en = "Conda Environment Cleanup - Interactive Selection (↑↓ move, Space select, Enter confirm)"
            stdscr.addstr(0, 0, title, curses.A_BOLD)
            stdscr.addstr(1, 0, title_en, curses.A_DIM)
            
            # 分隔线 / Separator
            stdscr.addstr(2, 0, "=" * min(width, 80))
            
            # 表头 / Table header
            header = f"{'':<2} {'选择':<4} {'环境名称':<20} {'状态':<15}"
            stdscr.addstr(3, 0, header, curses.A_UNDERLINE)
            
            # 计算显示范围 / Calculate display range
            max_display = height - 8  # 为conda clean选项留出空间 / Leave space for conda clean option
            start_idx = max(0, selected_idx - max_display // 2)
            if selected_idx < len(envs):  # 选择的是环境 / Selecting environment
                end_idx = min(len(envs), start_idx + max_display)
            else:  # 选择的是conda clean选项 / Selecting conda clean option
                end_idx = len(envs)
                start_idx = max(0, end_idx - max_display)
            
            # 显示环境列表 / Display environment list
            for i in range(start_idx, end_idx):
                env = envs[i]
                line_idx = i - start_idx + 4
                
                if line_idx >= height - 4:
                    break
                
                # 光标指示 / Cursor indicator
                cursor = "▶" if i == selected_idx else " "
                
                # 选择状态 / Selection state
                selected = "[✓]" if i in selected_indices else "[ ]"
                
                # 环境状态 / Environment status
                status = "活跃/Active" if env.is_active else "未激活/Inactive"
                
                # 行内容 / Line content
                line = f"{cursor:<2} {selected:<4} {env.name:<20} {status:<15}"
                
                # 高亮当前行 / Highlight current line
                if i == selected_idx:
                    stdscr.addstr(line_idx, 0, line, curses.A_REVERSE)
                else:
                    stdscr.addstr(line_idx, 0, line)
            
            # conda clean选项 / conda clean option
            clean_line_idx = min(height - 3, len(envs) - start_idx + 4)
            if clean_line_idx < height - 1:
                clean_cursor = "▶" if selected_idx == len(envs) else " "
                clean_selected = "[✓]" if run_clean else "[ ]"
                clean_text = f"{clean_cursor:<2} {clean_selected:<4} 执行 conda clean --all -y (清理所有缓存包)"
                if selected_idx == len(envs):
                    stdscr.addstr(clean_line_idx, 0, clean_text, curses.A_REVERSE)
                else:
                    stdscr.addstr(clean_line_idx, 0, clean_text)
            
            # 底部信息 / Bottom info
            bottom_line = height - 1
            info = f"已选择 {len(selected_indices)}/{len(envs)} 个环境 | 空格:选择/取消 上下:移动 Enter:确认 q:退出"
            if bottom_line > 0:
                stdscr.addstr(bottom_line, 0, info[:width-1], curses.A_DIM)
            
            stdscr.refresh()
        
        def main_curses(stdscr):
            curses.curs_set(0)  # 隐藏光标 / Hide cursor
            stdscr.keypad(True)  # 启用特殊键 / Enable special keys
            
            selected_idx = 0
            selected_indices = set()
            run_clean = True  # 默认选中 / Default selected
            
            while True:
                draw_menu(stdscr, selected_idx, selected_indices, run_clean)
                key = stdscr.getch()
                
                if key == curses.KEY_UP:
                    selected_idx = max(0, selected_idx - 1)
                elif key == curses.KEY_DOWN:
                    selected_idx = min(len(envs), selected_idx + 1)  # 包括conda clean选项 / Include conda clean option
                elif key == ord(' '):  # 空格键切换选择 / Space to toggle selection
                    if selected_idx < len(envs):
                        # 切换环境选择 / Toggle environment selection
                        if selected_idx in selected_indices:
                            selected_indices.remove(selected_idx)
                        else:
                            selected_indices.add(selected_idx)
                    else:
                        # 切换conda clean选项 / Toggle conda clean option
                        run_clean = not run_clean
                elif key == ord('\n') or key == ord('\r'):  # Enter键确认 / Enter to confirm
                    break
                elif key == ord('q') or key == ord('Q'):  # q键退出 / q to quit
                    selected_indices.clear()
                    run_clean = False
                    break
                elif key == ord('a') or key == ord('A'):  # a键全选 / a to select all
                    selected_indices = set(range(len(envs)))
                elif key == ord('d') or key == ord('D'):  # d键取消全选 / d to deselect all
                    selected_indices.clear()
            
            # 返回选择的环境和conda clean选项 / Return selected environments and conda clean option
            return [envs[i] for i in selected_indices], run_clean
        
        # 运行curses界面 / Run curses interface
        return curses.wrapper(main_curses)
        
    except ImportError:
        # 如果curses不可用，使用rich或基本界面 / If curses not available, use rich or basic interface
        if RICH_AVAILABLE:
            console = Console()
            console.print("[yellow]curses库不可用，使用基本选择界面[/yellow]")
            console.print("[yellow]curses library not available, using basic selection interface[/yellow]")
        selected_envs = basic_cli_select(envs)
        # 在基本界面中询问是否执行conda clean / Ask about conda clean in basic interface
        run_clean = True  # 默认选中 / Default selected
        if RICH_AVAILABLE:
            run_clean = Confirm.ask("是否执行 conda clean --all -y 清理所有缓存包?", default=True)
        else:
            response = input("是否执行 conda clean --all -y 清理所有缓存包? (y/n, 默认y): ").strip().lower()
            run_clean = response in ['', 'y', 'yes']
        return selected_envs, run_clean
    except Exception as e:
        # 任何错误都回退到基本界面 / Fall back to basic interface on any error
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[red]交互式界面错误: {e}[/red]")
            console.print("[yellow]使用基本选择界面[/yellow]")
        selected_envs = basic_cli_select(envs)
        run_clean = True
        return selected_envs, run_clean


def basic_cli_select(envs: List[CondaEnv]) -> Tuple[List[CondaEnv], bool]:
    """
    基本命令行界面选择 / Basic CLI selection
    
    Args:
        envs: Conda环境列表 / List of Conda environments
        
    Returns:
        Tuple[List[CondaEnv], bool]: (用户选择的环境列表, 是否执行conda clean) /
        (List of environments selected by user, whether to run conda clean)
    """
    console = Console() if RICH_AVAILABLE else None
    
    if console:
        console.print("\n[bold yellow]基本选择模式[/bold yellow]")
        console.print("[yellow]请输入要删除的环境编号（多个编号用逗号分隔）[/yellow]")
        console.print("[yellow]Enter environment numbers to delete (comma-separated)[/yellow]\n")
    else:
        print("\n基本选择模式 / Basic selection mode")
        print("请输入要删除的环境编号（多个编号用逗号分隔）")
        print("Enter environment numbers to delete (comma-separated)\n")
    
    # 显示环境列表 / Display environment list
    for i, env in enumerate(envs, 1):
        status = "活跃/Active" if env.is_active else "未激活/Inactive"
        if console:
            status_display = f"[green]{status}[/green]" if env.is_active else f"[dim]{status}[/dim]"
            console.print(f"{i:>3}. {env.name:<20} {status_display}")
        else:
            print(f"{i:>3}. {env.name:<20} {status}")
    
    # 获取用户输入 / Get user input
    while True:
        try:
            if console:
                selection = Prompt.ask("\n请输入环境编号", default="")
            else:
                selection = input("\n请输入环境编号: ").strip()
            
            if not selection:
                return []
            
            # 解析输入 / Parse input
            indices = []
            for part in selection.split(','):
                part = part.strip()
                if '-' in part:
                    # 处理范围 / Handle range
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    indices.extend(range(start, end + 1))
                else:
                    indices.append(int(part))
            
            # 验证索引 / Validate indices
            selected_envs = []
            for idx in indices:
                if 1 <= idx <= len(envs):
                    selected_envs.append(envs[idx - 1])
                else:
                    if console:
                        console.print(f"[red]错误：编号 {idx} 超出范围 (1-{len(envs)})[/red]")
                    else:
                        print(f"错误：编号 {idx} 超出范围 (1-{len(envs)})")
                    raise ValueError("索引超出范围")
            
            # 询问是否执行conda clean / Ask about conda clean
            run_clean = True  # 默认选中 / Default selected
            if console:
                run_clean = Confirm.ask("是否执行 conda clean --all -y 清理所有缓存包?", default=True)
            else:
                response = input("是否执行 conda clean --all -y 清理所有缓存包? (y/n, 默认y): ").strip().lower()
                run_clean = response in ['', 'y', 'yes']
            
            return selected_envs, run_clean
            
        except (ValueError, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                if console:
                    console.print("\n[yellow]操作已取消 / Operation cancelled[/yellow]")
                else:
                    print("\n操作已取消 / Operation cancelled")
                return [], False
            
            if console:
                console.print("[red]输入无效，请重新输入 / Invalid input, please try again[/red]")
            else:
                print("输入无效，请重新输入 / Invalid input, please try again")
            continue


def main() -> None:
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description="Conda环境清理工具 / Conda Environment Cleanup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例 / Examples:
  %(prog)s                    # 交互式选择环境进行清理 / Interactive environment selection
  %(prog)s --list             # 仅列出环境，不进行删除 / List environments only, no deletion
  %(prog)s --help             # 显示帮助信息 / Show help message
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="仅列出conda环境，不进行交互式选择 / List conda environments only, no interactive selection"
    )
    
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="自动确认删除，无需交互式确认 / Automatically confirm deletion, no interactive confirmation"
    )
    
    parser.add_argument(
        "--basic", "-b",
        action="store_true",
        help="使用基本命令行界面，不使用rich交互式界面 / Use basic CLI interface, not rich interactive interface"
    )
    
    args = parser.parse_args()
    
    # 获取环境列表 / Get environment list
    envs = get_conda_envs()
    
    if args.list:
        # 仅列出环境 / List environments only
        print_env_list(envs)
        return
    
    print(f"找到 {len(envs)} 个conda环境 / Found {len(envs)} conda environments")
    
    if not envs:
        print("没有可清理的环境 / No environments to clean")
        return
    
    # 选择环境 / Select environments
    if args.basic or not RICH_AVAILABLE:
        selected_envs, run_clean = basic_cli_select(envs)
    else:
        selected_envs, run_clean = interactive_select_envs(envs)
    
    if not selected_envs:
        print("未选择任何环境，操作取消 / No environments selected, operation cancelled")
        return
    
    # 显示选择结果 / Display selection results
    console = Console() if RICH_AVAILABLE else None
    if console:
        console.print(f"\n[bold yellow]已选择 {len(selected_envs)} 个环境进行删除:[/bold yellow]")
        for env in selected_envs:
            status = "[green]活跃/Active[/green]" if env.is_active else "[dim]未激活/Inactive[/dim]"
            console.print(f"  • {env.name} {status}")
        if run_clean:
            console.print("[bold yellow]将执行 conda clean --all -y 清理所有缓存包[/bold yellow]")
    else:
        print(f"\n已选择 {len(selected_envs)} 个环境进行删除:")
        for env in selected_envs:
            status = "活跃/Active" if env.is_active else "未激活/Inactive"
            print(f"  • {env.name} ({status})")
        if run_clean:
            print("将执行 conda clean --all -y 清理所有缓存包")
    
    # 确认删除 / Confirm deletion
    if not args.yes:
        if console:
            confirm = Confirm.ask("\n确认删除这些环境？")
        else:
            response = input("\n确认删除这些环境？(y/n): ").lower()
            confirm = response in ['y', 'yes']
        
        if not confirm:
            print("操作已取消 / Operation cancelled")
            return
    
    # 删除环境 / Delete environments
    delete_envs(selected_envs)
    
    # 执行conda clean --all -y / Execute conda clean --all -y
    if run_clean:
        conda_clean_all()
    
    print("\n操作完成 / Operation completed")


def conda_clean_all() -> None:
    """
    执行conda clean --all -y命令 / Execute conda clean --all -y command
    """
    console = Console() if RICH_AVAILABLE else None
    
    if console:
        console.print("\n[bold yellow]执行 conda clean --all -y 清理所有缓存包...[/bold yellow]")
    else:
        print("\n执行 conda clean --all -y 清理所有缓存包...")
    
    try:
        result = subprocess.run(
            ["conda", "clean", "--all", "-y"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True
        )
        
        if console:
            console.print("[green]✓ conda clean 执行成功[/green]")
        else:
            print("✓ conda clean 执行成功")
            
        # 显示命令输出 / Show command output
        if result.stdout:
            if console:
                console.print(f"[dim]输出: {result.stdout.strip()[:200]}...[/dim]")
            else:
                print(f"输出: {result.stdout.strip()[:200]}...")
                
    except subprocess.CalledProcessError as e:
        if console:
            console.print("[red]✗ conda clean 执行失败[/red]")
            console.print(f"[red]错误: {e.stderr.strip()}[/red]")
        else:
            print("✗ conda clean 执行失败")
            print(f"错误: {e.stderr.strip()}")
    except Exception as e:
        if console:
            console.print("[red]✗ conda clean 执行时发生未知错误[/red]")
            console.print(f"[red]错误: {str(e)}[/red]")
        else:
            print("✗ conda clean 执行时发生未知错误")
            print(f"错误: {str(e)}")


def delete_envs(envs: List[CondaEnv]) -> None:
    """
    删除指定的conda环境 / Delete specified conda environments
    
    Args:
        envs: 要删除的Conda环境列表 / List of Conda environments to delete
    """
    console = Console() if RICH_AVAILABLE else None
    
    for i, env in enumerate(envs, 1):
        if console:
            console.print(f"\n[{i}/{len(envs)}] 正在删除环境: [bold]{env.name}[/bold]")
        else:
            print(f"\n[{i}/{len(envs)}] 正在删除环境: {env.name}")
        
        try:
            # 执行conda env remove命令 / Execute conda env remove command
            result = subprocess.run(
                ["conda", "env", "remove", "-y", "-n", env.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True
            )
            
            if console:
                console.print(f"[green]✓ 环境 {env.name} 删除成功[/green]")
            else:
                print(f"✓ 环境 {env.name} 删除成功")
                
            # 显示命令输出 / Show command output
            if result.stdout:
                if console:
                    console.print(f"[dim]输出: {result.stdout.strip()}[/dim]")
                else:
                    print(f"输出: {result.stdout.strip()}")
                    
        except subprocess.CalledProcessError as e:
            if console:
                console.print(f"[red]✗ 环境 {env.name} 删除失败[/red]")
                console.print(f"[red]错误: {e.stderr.strip()}[/red]")
            else:
                print(f"✗ 环境 {env.name} 删除失败")
                print(f"错误: {e.stderr.strip()}")
        except Exception as e:
            if console:
                console.print(f"[red]✗ 环境 {env.name} 删除时发生未知错误[/red]")
                console.print(f"[red]错误: {str(e)}[/red]")
            else:
                print(f"✗ 环境 {env.name} 删除时发生未知错误")
                print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
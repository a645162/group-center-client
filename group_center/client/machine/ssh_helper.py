import curses


def main_interface(stdscr):
    # 清屏
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()

    # 创建窗口
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0, 0)

    # 绘制边框
    win.box()

    # 在窗口中显示文本
    win.addstr(1, 2, "欢迎来到Python TUI示例！")
    win.addstr(3, 2, "按 'q' 退出")

    # 刷新窗口
    win.refresh()

    # 处理按键
    while True:
        key = win.getch()
        if key == ord('q'):
            break


def init_tui():
    # 初始化curses
    curses.wrapper(main_interface)


def main():
    init_tui()


if __name__ == "__main__":
    main()

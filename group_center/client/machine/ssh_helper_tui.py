import os
import platform
import curses
import signal
import sys
from typing import List, Any

system_name = platform.system()

is_linux = system_name == "Linux"
is_root_user = is_linux and os.geteuid() == 0

wait_key_input = True


class TuiItem:
    """TUI item representation.

    Attributes:
        text (str): The display text of the item.
        x (int): The x-coordinate position.
        y (int): The y-coordinate position.
        key (str): The activation key for this item.
        color (int): The color code for display.
    """

    text: str = ""
    x: int = -1
    y: int = -1
    key: str = ""
    color: int = 0

    def __init__(self, text: str, key: str = "", handler=None, color: int = -1) -> None:
        """Initialize a TuiItem instance.

        Args:
            text (str): The display text.
            key (str, optional): Activation key. Defaults to "".
            handler (callable, optional): Action handler. Defaults to None.
            color (int, optional): Color code. Defaults to -1.
        """
        self.text = text
        self.key = key
        self.handler = handler
        self.color = color

    def try_to_handle(self) -> None:
        """Execute the associated handler if available."""
        if self.handler:
            self.handler()


def generate_new_ssh_key() -> None:
    """Generate a new SSH key pair using the system's ssh-keygen command."""
    os.system("ssh-keygen")


def backup_current_user() -> None:
    """Backup current user's SSH configuration.

    Currently not implemented. Place holder function only."""


def restore_current_user() -> None:
    """Restore current user's SSH configuration.

    Currently not implemented. Place holder function only."""


def get_all_user_list() -> List[str]:
    """Retrieve a list of all system users.

    Returns:
        List[str]: A list containing usernames of all system users.
    """
    result: List[str] = ["root"]

    # Walk "/home"
    for root, dirs, files in os.walk("/home"):
        for dir_name in dirs:
            result.append(dir_name)

    return result


def backup_all_user() -> None:
    """Backup SSH configuration for all users.

    Currently not implemented. Place holder function only."""


def restore_all_user() -> None:
    """Restore SSH configuration for all users.

    Currently not implemented. Place holder function only."""


def init_main_interface_content() -> List[TuiItem]:
    """Initialize and return the main interface content as a list of TuiItems.

    Returns:
        List[TuiItem]: A list containing all TuiItem instances for display.
    """
    str_list: List[TuiItem] = []

    str_list.append(TuiItem("SSH Helper - Group Center Client", color=1))
    str_list.append(TuiItem(""))

    str_list.append(TuiItem(f"System:{system_name}"))
    if is_root_user:
        str_list.append(TuiItem("With 'root' user to run this program"))

    str_list.append(TuiItem(""))

    # str_list.append(TuiItem("Generate New 'SSH key'", key="c", handler=generate_new_ssh_key))

    str_list.append(
        TuiItem("Backup Current User", key="1", handler=backup_current_user)
    )
    str_list.append(
        TuiItem("Restore Current User", key="2", handler=restore_current_user)
    )

    if is_root_user:
        str_list.append(
            TuiItem("Backup All User(Root Only)", key="3", handler=backup_current_user)
        )
        str_list.append(
            TuiItem(
                "Restore All User(Root Only)", key="4", handler=restore_current_user
            )
        )

    str_list.append(TuiItem(""))
    str_list.append(TuiItem("Exit", key="q", handler=lambda: exit(0)))

    return str_list


def main_interface(stdscr) -> None:
    """Main interface rendering function using curses.

    Args:
        stdscr: The main window object provided by curses.
    """
    # Clear screen
    stdscr.clear()

    # Set up the screen
    # Hide the cursor
    curses.curs_set(0)
    # Disable the input buffer
    stdscr.nodelay(1)

    # Create a new window
    height, width = stdscr.getmaxyx()
    win = curses.newwin(height, width, 0, 0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
    item_with_key_color_index = 3

    # Draw a box around the window
    win.box()

    # Init content
    tui_list = init_main_interface_content()
    for i, tui_item in enumerate(tui_list):
        key_tip = ""
        if tui_item.key:
            key_tip = f"({tui_item.key})"

        if tui_item.color > 0:
            win.addstr(
                i + 1, 2, key_tip + tui_item.text, curses.color_pair(tui_item.color)
            )
        else:
            if tui_item.key:
                win.addstr(
                    i + 1,
                    2,
                    key_tip + tui_item.text,
                    curses.color_pair(item_with_key_color_index),
                )
            else:
                win.addstr(i + 1, 2, key_tip + tui_item.text)

    # Refresh the window
    win.refresh()

    try:
        # Handle key input
        global wait_key_input
        while wait_key_input:
            key = win.getkey()

            for tui_item in tui_list:
                if not tui_item.key:
                    continue

                if key == tui_item.key:
                    tui_item.try_to_handle()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def signal_handler(signal: int, frame: Any) -> None:
    """Handle system signals to clean up resources before exit."""
    global wait_key_input
    wait_key_input = False

    sys.exit(0)


def init_tui() -> None:
    """Initialize the TUI environment and setup signal handlers."""
    # Register the signal handler
    # Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Init curses
    curses.wrapper(main_interface)


def main() -> None:
    """Main entry point for the TUI application."""
    init_tui()


if __name__ == "__main__":
    main()

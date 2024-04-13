import os
import contextlib

os.system("")


class ColorProperty:
    colors = (
        "red",
        "green",
        "cyan",
        "blue",
        "black",
        "magenta",
        "white",
        "yellow",
        "blank",
    )
    fg_colors_dict = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    bg_colors_dict = {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
        "blank": "",
    }

    def __init__(self, default_fg_color, default_bg_color) -> None:
        if default_fg_color is not None and (
            default_fg_color not in self.colors or default_fg_color == "blank"
        ):
            raise ValueError(
                f"default foreground color {default_fg_color} is unsupported"
            )
        if default_bg_color is not None and default_bg_color not in self.colors:
            raise ValueError(
                f"default background color {default_bg_color} is unsupported"
            )
        self.default_fg_color = default_fg_color
        self.default_bg_color = default_bg_color

        self._fg_color = None
        self._bg_color = None

    @property
    def fg_color(self):
        return self._fg_color or self.default_fg_color

    @fg_color.setter
    def fg_color(self, color):
        if color not in self.colors:
            raise ValueError(f"color {color} not supported by terminal")
        self._fg_color = color

    @property
    def bg_color(self):
        return self._bg_color or self.default_bg_color

    @bg_color.setter
    def bg_color(self, color):
        if color is not None and color not in self.colors:
            raise ValueError(f"color {color} not supported by terminal")
        self._bg_color = color

    @property
    def final_color(self):
        return self.fg_colors_dict[self.fg_color] + self.bg_colors_dict[self.bg_color]


class Font:
    reset_font = "\033[0m"
    bold_font = "\033[1m"
    faint_font = "\033[2m"
    italics_font = "\033[3m"
    underline_font = "\033[4m"
    slow_blink_font = "\033[5m"
    rapid_blink_font = "\033[6m"
    invert_font = "\033[7m"
    hide_font = "\033[8m"
    strike_font = "\033[9m"


class TerminalCursor:

    def __init__(self, end_chars="\n") -> None:
        self.end_chars = end_chars

    def toggle(self, visiblity):
        if visiblity:
            print("\033[?25h", end="")
        else:
            print("\033[?25l", end="")

    def move_up(self, by):
        end = self.end_chars
        if not by:
            return
        print(f"\033[{by}A", end=end)

    def move_down(self, by):
        end = self.end_chars
        if not by:

            return
        print(f"\033[{by}B", end=end)

    def move_left(self, by):
        end = self.end_chars
        if not by:
            return
        print(f"\033[{by}D", end=end)

    def move_right(self, by):
        end = self.end_chars
        if not by:
            return
        print(f"\033[{by}C", end=end)

    def set_cursor_position(self, x, y):
        end = self.end_chars
        print(f"\033[{x};{y}H", end=end)


@contextlib.contextmanager
def terminal_cursor(visible=None, end="\n"):
    crsr = TerminalCursor(end_chars=end)
    if visible:
        crsr.toggle(visiblity=visible)
    try:
        yield crsr
    finally:
        if visible:
            crsr.toggle(visiblity=not visible)

import time
import io

old_print = print


def sleep(_time):
    time.sleep(_time)


def new_print(*args, sep=" ", file=None, **kwargs):
    kwargs.pop("flush", False)
    for arg in args:
        for c in str(arg):
            old_print(c, file=file, end="", flush=True)
            time.sleep(0.02)
        if len(args) > 1:
            old_print(sep, file=file, end="")

    time.sleep(0.2)
    old_print(**kwargs, flush=True)


print = new_print


def print_backwards(*args, sep=" ", file=None, **kwargs):
    _file = io.StringIO()
    old_print(*args, sep=sep, file=_file, end="", **kwargs)
    _str = _file.getvalue()

    size = len(_str)
    _new_str = _str
    time.sleep(0.2)
    for i in range(size + 1):
        old_print("\r" + _new_str[: (size - i)] + " " * i, end="")
        old_print("\r" + _new_str[: (size - i)], end="", flush=True)
        time.sleep(0.02)

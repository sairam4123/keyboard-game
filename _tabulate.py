from io import StringIO

from typing import Generator, Sequence, SupportsInt
from itertools import zip_longest

def replace_none_with[T](*vals: Sequence[T | None], fillvalue: T = "") -> Generator[tuple[T, ...], None, None]:
    for val in vals:
        yield tuple((fillvalue if col is None else col) for col in val)


def replace_none[T](*vals: T | None, fillvalue: T = "") -> Generator[T, None, None]:
    yield from ((fillvalue if col is None else col) for col in vals)


string = "─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬"

class Table:
    def __init__(self, *values) -> None:
        self.values = values
        self.headings = None
        self.padding = 2
        self.empty_default = " "
        self.empty_heading = "Untitled"
    
    def with_headings(self, *headings):
        self.headings = headings
        return self
    
    def with_padding(self, padding: int = 2):
        self.padding = padding or self.padding
        return self
    
    def with_default(self, empty_default = ""):
        self.empty_default = empty_default or self.empty_default
        return self
    
    def with_default_heading(self, empty_heading: str = ""):
        self.empty_heading = empty_heading
        return self
    
    def __str__(self) -> str:
        return tabulates(*self.values, padding=self.padding, headings=self.headings, empty_default=self.empty_default, empty_heading=self.empty_heading).strip()


def tabulate(*values: Sequence[str | None]):
    return Table(*values)


def _tabulate(
    *_values: Sequence[str | None],
    padding: SupportsInt = 2,
    headings: Sequence[str | None] | None = None,
    empty_default: str = " ",
    empty_heading: str = "Untitled",
    file=None,
):
    headings = headings or []
    vals: Sequence[Sequence[str]] = list(
        zip_longest(
            *zip_longest(*replace_none_with(*_values, fillvalue=empty_default), fillvalue=empty_default),
            fillvalue=empty_default,
        )
    )
    if headings:
        vals: Sequence[Sequence[str]] = list(
            zip_longest(
                replace_none(*headings, fillvalue=empty_heading),
                *vals,
                fillvalue=empty_default,
            )
        )
    t_values: Sequence[Sequence[str]] = list(zip(*vals))

    sizes = _calculate_sizes(*vals, padding=padding)
    print("╔" + "╤".join(["═" * size for size in sizes]) + "╗", file=file)
    for row_idx, row in enumerate(t_values):
        print("║", end="", file=file)
        for col_idx, (size, col) in enumerate(zip(sizes, row)):
            if row_idx < 1 and headings:
                print("\033[1m" + col.center(size), end="\033[0m", file=file)
            else:
                print(col.center(size), end="", file=file)

            if col_idx < (len(t_values[row_idx]) - 1):
                print("│", end="", file=file)
        print("║", file=file)
        if row_idx < 1 and headings:
            print("╠" + "╪".join(["═" * size for size in sizes]), end="╣\n", file=file)
        elif row_idx < len(vals[0]) - 1:
            print("╟" + "┼".join(["─" * size for size in sizes]), end="╢\n", file=file)

    print("╚" + "╧".join(["═" * size for size in sizes]) + "╝", file=file)
    return file


def tabulates(
    *values: Sequence[str | None],
    padding: SupportsInt = 2,
    headings: Sequence[str | None] | None = None,
    empty_default: str = " ",
    **kwargs,
) -> str:
    with StringIO() as buf:
        _tabulate(
            *values,
            padding=padding,
            headings=headings,
            empty_default=empty_default,
            file=buf,
            **kwargs,
        )
        return buf.getvalue()


def _calculate_sizes(*values: Sequence[str], padding: SupportsInt = 2) -> Sequence[int]:
    sizes = []
    for value in values:
        longest = len(max(value, key=len))
        cell_size = int(padding) + longest + int(padding)
        sizes.append(cell_size)
    return sizes


if __name__ == "__main__":

    # from t import print as p
    print(
        tabulate(
            ["Hello", "This is a test.", "Cool"],
            ["This is cool stuff", "Test Cool"],
            [None, None, "Cool stuff"],
        )
        # .with_headings("Systems", "Invitations", None)
        .with_padding(5)
        .with_default("N/A")
        .with_default_heading("Untitled")
    )

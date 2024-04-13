import keyboard
from terminal import ColorProperty, Font, terminal_cursor


class MenuConfig:
    def __init__(self) -> None:
        self.selected_color = ColorProperty("blue", "black")
        self.color = ColorProperty("white", "blank")
        self.prompt = ">"
        self.right_prompt = None
        self.description = None
        self.padding = 2

    def calculate_prompt(self):
        return (
            self.padding * " "
            + self.selected_color.final_color
            + self.prompt
            + Font.reset_font
            + self.padding * " "
        )

    def calculate_prompt_size(self):
        return self.padding + len(self.prompt) + self.padding

    def calculate_right_prompt(self):
        if not self.right_prompt:
            return ""
        return (
            self.padding * " "
            + self.selected_color.final_color
            + self.right_prompt
            + Font.reset_font
            + self.padding * " "
        )

    def calculate_right_prompt_size(self):
        if not self.right_prompt:
            return 0
        return self.padding + len(self.right_prompt)


def menu(*values: str, config: MenuConfig, title: str = ""):
    color = config.color.final_color
    selection_color = config.selected_color.final_color

    selected_choice = values[0]

    idx = 0
    should_exit = False
    wait = False

    def up_arrow_event():
        nonlocal idx, selected_choice, wait
        idx = (idx - 1) % len(values)
        selected_choice = values[idx]
        wait = False

    def down_arrow_event():
        nonlocal idx, selected_choice, wait
        idx = (idx + 1) % len(values)
        selected_choice = values[idx]
        wait = False

    def enter_event():
        nonlocal should_exit, wait
        should_exit = True
        wait = False

    def escape_event():
        nonlocal should_exit, wait, selected_choice
        selected_choice = None
        should_exit = True
        wait = False

    def wait_for_input():
        nonlocal wait
        wait = True
        while wait:
            continue

    keyboard.add_hotkey("up", up_arrow_event, suppress=True)
    keyboard.add_hotkey("down", down_arrow_event, suppress=True)
    keyboard.add_hotkey("enter", enter_event, suppress=True)
    keyboard.add_hotkey("escape", escape_event, suppress=True)

    clear_length = max(map(len, (title,) + values))
    prompt_size = config.calculate_prompt_size() * " "
    right_prompt_size = config.calculate_right_prompt_size() * " "
    clear_size = clear_length * " "

    BOLD = Font.bold_font
    BOLD_UNDERLINED = Font.bold_font + Font.underline_font
    RESET = Font.reset_font

    with terminal_cursor(visible=False) as crsr:
        while not should_exit:
            print("\r" + BOLD + title + RESET)
            for value in values:
                if selected_choice == value:
                    print("\r" + config.calculate_prompt(), end="")
                    print(BOLD_UNDERLINED + selection_color + value + RESET, end="")

                    if config.right_prompt:
                        print(config.calculate_right_prompt() + RESET + clear_size)
                    else:
                        print(clear_size)
                else:
                    print("\r" + prompt_size + color, end="")
                    print(value + right_prompt_size + clear_size + RESET)

            crsr.move_up(len(values) + 2)
            wait_for_input()

        for _ in range(len(values) + 1):
            print(clear_size)
        crsr.move_up(len(values) + 2)
    return selected_choice


if __name__ == "__main__":
    config = MenuConfig()
    config.selected_color.bg_color = "blank"
    config.prompt = ">>"
    config.padding = 2
    # config.right_prompt = "<<"

    choices = ["Python", "JS", "Java", "Kotlin", "Go", "PASCAL", "C", "COBOL"]

    choice = ""
    lang = ""

    while choice != "Yes":
        lang = menu(*choices, title="Select a language to learn:", config=config)
        print("Selected language:", lang)
        choice = menu("Yes", "No", title="Are you sure?", config=config)
        with terminal_cursor() as crsr:
            crsr.move_up(2)

    print("Selected language:", lang)
    print("Confirming language:", lang)
    exit(0)

import keyboard
from fuzzywuzzy import process
import logging
import math

from t import print
from terminal import Font, terminal_cursor

logging.getLogger("root").setLevel(level=logging.ERROR)

key_dict = {
    "space": " ",
    "backspace": "\b \b",
    "enter": "\n",
    "up": "",
    "down": "",
    "left": "",
    "right": "",
}

options = {"CFEPWDR-HB", "CFEPWDR-PR", "APLM-MELKU"}


def autocomplete(*options, prompt: str):

    phrase = ""
    print(prompt.strip() + " ", end="", flush=True)

    idx = len(phrase)

    choice_idx = 0
    reset = False
    with terminal_cursor(end="") as crsr:
        while True:
            if keyboard.is_pressed("esc"):
                break
            if (not phrase) and reset:
                choice_idx = 0
                reset = False
            choices = process.extract(phrase, choices=options)
            key = keyboard.read_event(True)
            if key.event_type == "up":
                continue
            if keyboard.is_modifier(key.name):
                continue
            key_str = key_dict.get(key.name, key.name)
            if key_str == "esc":
                print()
                break
            if key_str == "\n":
                crsr.move_left(len(phrase))
                print(choices[choice_idx][0], end="")
                print(key_str, end="")
                phrase = choices[choice_idx][0]
                idx = len(phrase) - 1
                break
            if key.name in ["up", "down"]:
                if key.name == "down":
                    choice_idx = (choice_idx + 1) % len(choices)
                    crsr.move_left(len(phrase))
                    print(Font.faint_font + choices[choice_idx][0], end="", flush=True)
                    crsr.move_left(len(choices[choice_idx][0]))
                    print(Font.reset_font + phrase, end="", flush=True)
                # Todo implement select menu style.
                continue
            if key.name in ["left", "right"]:
                # continue
                if key.name == "left":
                    if idx == 0:
                        continue
                    idx -= 1

                if key.name == "right":
                    if idx == len(phrase) - 1:
                        continue
                    idx += 1

            if key.name in ["tab", "end"]:
                crsr.move_left(len(phrase))
                phrase = choices[choice_idx][0]
                print(Font.reset_font + phrase, end="", flush=True)
                idx = len(phrase) - 1
                continue

            if key.name not in ["backspace", "up", "down", "left", "right"]:
                crsr.move_left(len(phrase))
                phrase += key_str.upper()
                idx += 1
            elif key.name == "backspace":
                reset = True
                crsr.move_left(len(phrase))
                phrase = phrase[:-1]
                idx -= 1
            else:
                crsr.move_left(len(phrase))

            print(Font.faint_font + choices[choice_idx][0], end="", flush=True)
            crsr.move_left(len(choices[choice_idx][0]))
            print(Font.reset_font + phrase, end="", flush=True)
            crsr.move_left(len(phrase))

            crsr.move_right(idx)
    return phrase


prodID = autocomplete(*options, prompt="Enter Prod ID:")

print(f"PROD ID you entered is: {prodID}")

from contextlib import contextmanager
import keyboard
import time
from pynput.keyboard import Key, Controller
from win32api import GetKeyState
from win32con import VK_CAPITAL, VK_SCROLL, VK_NUMLOCK
import threading
import requests
import random
from fuzzywuzzy import fuzz

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from pydub.playback import play
import gtts

from pathlib import Path

TTS_AVAILABLE = True

def_sentences = """
Don't step on the broken glass.
Plans for this weekend include turning wine into water.
Malls are great places to shop; I can find everything I need under one roof.
The river stole the gods.
It was a slippery slope and he was willing to slide all the way to the deepest depths.
No matter how beautiful the sunset, it saddened her knowing she was one day older.
He picked up trash in his spare time to dump in his neighbor's yard.
Pat ordered a ghost pepper pie.
The truth is that you pay for your lifestyle in hours.
He hated that he loved what she hated about hate.
It doesn't sound like that will ever be on my travel list.
They did nothing as the raccoon attacked the lady�s bag of food.
He colored deep space a soft yellow.
You can't compare apples and oranges, but what about bananas and plantains?
The fox in the tophat whispered into the ear of the rabbit.
The beauty of the sunset was obscured by the industrial cranes.
People who insist on picking their teeth with their elbows are so annoying!
She had the gift of being able to paint songs.
Don't piss in my garden and tell me you're trying to help my plants grow.
He didn�t want to go to the dentist, yet he went anyway.
She found his complete dullness interesting.
25 years later, she still regretted that specific moment.
You bite up because of your lower jaw.
I come from a tribe of head-hunters, so I will never need a shrink.
He picked up trash in his spare time to dump in his neighbor's yard.
She wore green lipstick like a fashion icon.
There are no heroes in a punk rock band.
The rain pelted the windshield as the darkness engulfed us.
The door swung open to reveal pink giraffes and red elephants.
Never underestimate the willingness of the greedy to throw you under the bus.
He had a hidden stash underneath the floorboards in the back room of the house.
I currently have 4 windows open up� and I don�t know why.
It turns out you don't need all that stuff you insisted you did.
Behind the window was a reflection that only instilled fear.
He was the type of guy who liked Christmas lights on his house in the middle of July.
"""


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


def get_pleasantries(score):
    if score > 99:
        return "Perfect!"
    if score > 95 and score <= 99:
        return "Excellent!"
    if score > 89 and score <= 95:
        return "Good job!"
    if score > 85 and score <= 89:
        return "Not good! Try again!"
    if score <= 85:
        return "You failed! Try again!"


def tts(tts_message):
    global TTS_AVAILABLE

    if not TTS_AVAILABLE:
        return
    fp = Path.cwd() / "tts"
    fp.mkdir(parents=True, exist_ok=True)
    tts_file = fp / f"{random.randint(1000000, 99999999)}.mp3"
    try:
        gtts.gTTS(tts_message, lang="en").save(str(tts_file))
    except gtts.gTTSError:
        TTS_AVAILABLE = False
        return
    seg = AudioSegment.from_mp3(tts_file)
    try:
        play(seg)
    except (RuntimeError, CouldntDecodeError):
        TTS_AVAILABLE = False
        return


@contextmanager
def with_animation(callable):
    _stop = False

    def stop():
        return _stop

    thread = threading.Thread(target=callable, args=(stop,), daemon=True)
    thread.start()
    try:
        yield True
    finally:
        _stop = True
        thread.join()


@contextmanager
def get_new_words():
    _stop = False

    def request_new_sentence():
        while not _stop:
            with requests.get(
                "https://random-words-api-beta.vercel.app/word/sentence/"
            ) as res, open("sentences.txt", "a") as f:
                if res.status_code != 200:
                    break
                try:
                    sentence = res.json()[0]["word"] + "\n"
                    if len(sentence) > 88:
                        continue
                    f.write(sentence)
                except (IndexError, KeyError, TypeError):
                    continue
            time.sleep(2)

    thread = threading.Thread(target=request_new_sentence)
    thread.start()
    yield True
    _stop = True
    thread.join()


keyboard_2 = Controller()

key_dict = {
    "space": " ",
    "enter": "\n",
}

num_lock = GetKeyState(VK_NUMLOCK) > 0
scroll_lock = GetKeyState(VK_SCROLL) > 0
caps_lock = GetKeyState(VK_CAPITAL) > 0

if num_lock:
    keyboard_2.tap(Key.num_lock)
if scroll_lock:
    keyboard_2.tap(Key.scroll_lock)
if caps_lock:
    keyboard_2.tap(Key.caps_lock)


def waiting_anim(stop):
    while True:
        if stop():
            break
        time.sleep(0.3)
        keyboard_2.tap(Key.num_lock)
        time.sleep(0.3)
        keyboard_2.tap(Key.caps_lock)
        time.sleep(0.3)
        keyboard_2.tap(Key.scroll_lock)
        time.sleep(0.3)


def all_at_once():
    keyboard_2.tap(Key.num_lock)
    keyboard_2.tap(Key.caps_lock)
    keyboard_2.tap(Key.scroll_lock)
    time.sleep(0.2)


def bad_job():
    keyboard_2.tap(Key.caps_lock)
    time.sleep(0.2)
    keyboard_2.tap(Key.num_lock)
    keyboard_2.tap(Key.scroll_lock)
    time.sleep(0.2)


def quit_anim():
    keyboard_2.tap(Key.num_lock)
    time.sleep(0.2)
    keyboard_2.tap(Key.scroll_lock)
    time.sleep(0.2)


def get_phrase(og_phrase):
    phrase = ""
    elapsed = time.time()
    print(Font.faint_font + og_phrase, end="")
    print(f"\033[{len(og_phrase)}D", flush=True, end="")

    while True:
        key = keyboard.read_event()
        if key.event_type == "up":
            continue
        if key.name == "esc":
            print()
            break
        key_name: str = key_dict.get(key.name, key.name)
        if key.name == "enter":
            print(f"\033[{len(og_phrase)}D", end="")
            print(" " * len(og_phrase), end="")
            print("\r" + Font.reset_font + phrase, flush=True, end="")
            print()
            break
        print(f"\033[{len(phrase)}D", end="")
        print(
            Font.faint_font
            + og_phrase
            + Font.reset_font
            + Font.bold_font
            + f"\t({time.time()-elapsed:.2f})",
            flush=True,
            end="",
        )
        print("\r", end="")
        print(Font.reset_font + phrase, flush=True, end="")
        if key.name in [
            "backspace",
            "up",
            "down",
            "left",
            "right",
        ]:
            continue
        if key.name in ["alt", "shift", "ctrl", "left windows", "right windows", "tab"]:
            continue
        if key.name in [
            "caps lock",
            "num lock",
            "scroll lock",
        ]:
            continue
        print(f"\033[{len(phrase)}D", end="")
        print(
            Font.faint_font
            + og_phrase
            + Font.reset_font
            + Font.bold_font
            + f"\t({time.time()-elapsed:.2f})",
            flush=True,
            end="",
        )
        print("\r", end="")
        phrase += key_name.lower()
        print(Font.reset_font + phrase, flush=True, end="")
    return phrase, time.time() - elapsed


def read_sentences():
    with open("sentences.txt") as f:
        return f.readlines()


print("Welcome to Keyboard game!")
tts("Welcome to Keyboard game!")

tts("How many keyphrases would you like to type?")
keyboard_2.tap(Key.num_lock)
keyphrases = int(input("How many keyphrases would you like to type?: "))
keyboard_2.tap(Key.num_lock)

if keyphrases < 1:
    print("Keyphrases cannot go below zero. Defaulting to 1...")
    tts("Keyphrases cannot go below zero. Defaulting to 1...")
    keyphrases = 1
if keyphrases > 15:
    print("Maximum keyphrases is 15. You cannot go above that. Defaulting to 15...")
    tts("Maximum keyphrases is 15. You cannot go above that. Defaulting to 15...")
    keyphrases = 15

print(
    f"You will be asked to type {keyphrases} keyphrase{'s' if keyphrases > 1 else ''}.."
)
tts(f"You will be asked to type {keyphrases} keyphrase{'s' if keyphrases > 1 else ''}.")

print("Each keyphrase will be timed and you have to type quickly.")
tts("Each keyphrase will be timed and you have to type quickly.")

print("Backspaces are not allowed! You cannot edit the text you typed.")
tts("Backspaces are not allowed! You cannot edit the text you typed.")


file = Path.cwd() / "sentences.txt"
file.touch()

scores = []
for i in range(keyphrases):
    sentences = read_sentences()
    og_phrase = (
        random.choice(sentences or def_sentences.splitlines()).strip("\n").lower()
    )
    print(f"Enter the following keyphrase:\n{og_phrase}")
    tts("Enter the following keyphrase:")
    tts(og_phrase)
    try:
        with with_animation(waiting_anim), get_new_words():
            phrase, elapsed = get_phrase(og_phrase)
    except KeyboardInterrupt:
        print("Quiting!")
        tts("Quitting!")
        for i in range(8):
            quit_anim()
        break
    except Exception as e:
        print(f"Exception occurred.. ({e}) Quitting!")
        tts(f"Exception occurred.. {e} Quitting!")
        for i in range(8):
            quit_anim()
        break

    if phrase:
        tts("You typed: ")
        tts(phrase)

    partial_ratio = fuzz.partial_ratio(phrase, og_phrase)
    ratio = fuzz.ratio(og_phrase, phrase)
    score = (
        float(ratio) * 0.75 + float(partial_ratio) * 0.2 + float(elapsed / 1200) * 0.05
    )
    score = max(0, min(100, int(score)))
    scores.append((score, elapsed))
    pleasantry = get_pleasantries(score)
    if not phrase:
        print("Quiting!")
        tts("Quitting!")
        for i in range(8):
            quit_anim()
        break

    print(f"{pleasantry} You scored: {score} pts.")
    tts(f"{pleasantry} You scored: {score} points.")
    if score >= 89:
        for i in range(8):
            all_at_once()
    else:
        for i in range(8):
            bad_job()
tot_score = sum([_score[0] for _score in scores])
avg_score = tot_score / keyphrases
tot_time = sum([_score[1] for _score in scores])
avg_time = tot_time / keyphrases

print(f"You have completed {keyphrases} keyphrase{'s' if keyphrases > 1 else ''}..")
tts(f"You have completed {keyphrases} keyphrase{'s' if keyphrases > 1 else ''}..")

print(Font.bold_font + "Your stats are as follows: " + Font.reset_font)
tts("Your stats are as follows: ")

print(f"Your total score: {tot_score:.0f} pts.")
tts(f"Your total score is {tot_score:.0f} points.")
print(f"Your average score: {avg_score:.1f} pts.")
tts(f"Your average score is {avg_score:.1f} points.")
print(f"Your total time: {tot_time:.2f} secs.")
tts(f"Your total time is {tot_time:.2f} seconds.")
print(f"Your average time: {avg_time:.2f} secs. (Not subject to length differences.)")
tts(
    f"Your average time is {avg_time:.2f} seconds. (Not subject to length differences.)"
)

print("Thank you for trying out the keyboard game!")
tts("Thank you for trying out the keyboard game!")

new_num_lock = GetKeyState(VK_NUMLOCK) > 0
new_scroll_lock = GetKeyState(VK_SCROLL) > 0
new_caps_lock = GetKeyState(VK_CAPITAL) > 0

if new_num_lock:
    keyboard_2.tap(Key.num_lock)
if new_scroll_lock:
    keyboard_2.tap(Key.scroll_lock)
if new_caps_lock:
    keyboard_2.tap(Key.caps_lock)
if num_lock:
    keyboard_2.tap(Key.num_lock)
if scroll_lock:
    keyboard_2.tap(Key.scroll_lock)
if caps_lock:
    keyboard_2.tap(Key.caps_lock)

tts("Press any key to exit.")

tts_folder = Path.cwd() / "tts"
for item in tts_folder.iterdir():
    item.unlink()
tts_folder.rmdir()

import os

os.system("pause")

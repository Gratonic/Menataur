import subprocess
import sys

# note: this dictionary is global so that users are able to add their own custom colors to use
foreground_colors = {
"blue": "\033[34m", "light_blue": "\033[94m",
"cyan": "\033[36m", "light_cyan": "\033[96m",
"red": "\033[31m", "light_red": "\033[91m",
"green": "\033[32m", "light_green": "\033[92m",
"yellow": "\033[33m", "light_yellow": "\033[93m",
"magenta": "\033[35m", "light_magenta": "\033[95m",
"black": "\033[30m", "white": "\033[37m",
"gray": "\033[90m", "grey": "\033[90m",
"reset": "\033[0m"
}

def clear_terminal():
    if sys.platform == "linux":
        subprocess.run("clear", shell=True)
    elif sys.platform == "darwin":
        # for a MacOS, note: "command + k" like terminal clear
        sys.stdout.write('\033c')
        sys.stdout.flush()
    else:
        # for Windows and other obsolete operating systems
        subprocess.run("cls", shell=True)

def add_foreground_color(color_name: str, color_code: str) -> None:
    foreground_colors[color_name] = color_code

def validate_foreground_color(fore_color: str) -> str:
    color = fore_color.lower()
    if color in foreground_colors:
        return foreground_colors[color]
    else:
        print(f"{foreground_colors["red"]}[!] Error: {foreground_colors["yellow"]}{color}{foreground_colors["red"]} is not a valid/supported color in this program.{fore_reset}")
        print(f"{foreground_colors["green"]}The following colors are supported:{foreground_colors["reset"]}")
        for color_key in foreground_colors.keys():
            if color_key != "gray" or color_key != "grey":
                print(f"{foreground_colors[color_key]}{color_key}{foreground_colors["reset"]}")
            else:
                print(f"{foreground_colors[color_key]}gray/grey{foreground_colors["reset"]}")

        exit(1)

def paint_text(text: str, colors: list) -> str:
    # avoids waisting compute time with an algorithm if there is only one color provided
    if len(colors) == 1:
        return f"{validate_foreground_color(colors[0])}{text}{foreground_colors["reset"]}"

    # validates the colors and retrieves their actual color values
    colors = [validate_foreground_color(fore_color=color) for color in colors]
    # keeps track of the colors that are temporarily banned
    banned_colors = list()
    # creates a list of every character in the given text
    characters = list(text)

    for char in range(len(text)):
        # avoids waisting compute time on non-printable characters (with the needed exceptions)
        if characters[char] == " ":
            continue
        elif characters[char].isprintable() == True or characters[char] == "\\" or characters[char] == "\'" or characters[char] == '\"':
            pass
        else:
            continue

        if len(colors) < 1:
            colors = banned_colors.copy()

            banned_colors = []

        # fetch the color to use, use it for the current character, then add it to the banned_colors
        color = colors.pop()

        characters[char] = color + characters[char]

        banned_colors.append(color)

    # create the new text string
    text = "".join(characters)

    return f"{text}{foreground_colors["reset"]}"
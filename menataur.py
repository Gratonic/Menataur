r"""
# :: Author Information and Program Details :: #

File Name: menataur.py
Author(s): Gratonic (https://github.com/Gratonic) and FailurePoint (https://github.com/FailurePoint)
Language: Python 3.13.5
Dependencie(s): colorama
Last Modified: Septemeber 26, 2026

# :: Description :: #

This program was designed to make writing command-line menu interfaces easier. 
It splits each menu into blocks represented by classes. These block classes are combined to create 
a Menu instance, which can then be combined with other Menu instances within the Menataur class.
The Menataur class organizes the menu components and uses a custom navigation algorithm to allow 
users to move between them.

# :: Example Usage :: #

# create the banner
banner = Banner()

banner.title = 
___  ___                 _                   
|  \/  |                | |                  
| .  . | ___ _ __   __ _| |_ __ _ _   _ _ __ 
| |\/| |/ _ \ '_ \ / _` | __/ _` | | | | '__|
| |  | |  __/ | | | (_| | || (_| | |_| | |   
\_|  |_/\___|_| |_|\__,_|\__\__,_|\__,_|_|   
banner.title_colors = ["cyan", "yellow", "green", "magenta"]
banner.title_bar = "_________________________________________________/"
banner.title_bar_color = "blue"
banner.program_name = "Menataur"
banner.program_name_color = "blue"
banner.program_version_number = 1.0 
banner.program_version_number_color = "yellow"
banner.operating_system_support_message = "This Program Supports Linux, MacOS, and Windows"
banner.operating_system_support_message_color = "light_green"

# create the options
options = Options()

options.option_description_color = "white"
options.option_number_color = "light_yellow"
options.option_name_color = "cyan"
options.navigation_option_color = "light_red"

options.add_option("View Profile", 1, "Profile")
options.add_option("Settings", 2, "Settings")
options.add_option("Help", 3, "Help")

# create the prompt
prompt = Prompt()

prompt.prompt_message = "Select an option: "
prompt.prompt_message_color = "light_magenta"

# create and run the menu
menu = Menu()

menu.add_banner(banner)
menu.add_options(options)
menu.add_prompt(prompt)

menu.run_menu()

# you can only simply display it (excludes the input prompt)
menu.display_menu()
"""

# [=== Imports ===] #

from colorama import Fore, Back
from functools import partial
import subprocess
import random
import sys

# [=== Functions ===] #

def clear_terminal():
    # for Linux, MacOS, and Unix-Like operating systems
    if sys.platform in ("linux", "darwin"):
        subprocess.run("clear", shell=True)
    else:
        # for Windows and other obsolete operating systems
        subprocess.run("cls", shell=True)

def validate_foreground_color(fore_color: str) -> str:
    foreground_colors = {
        "blue": Fore.BLUE, "light_blue": Fore.LIGHTBLUE_EX, 
        "cyan": Fore.CYAN, "light_cyan": Fore.LIGHTCYAN_EX,
        "red": Fore.RED, "light_red": Fore.LIGHTRED_EX,
        "green": Fore.GREEN, "light_green": Fore.LIGHTGREEN_EX, 
        "yellow": Fore.YELLOW, "light_yellow": Fore.LIGHTYELLOW_EX,
        "magenta": Fore.MAGENTA, "light_magenta": Fore.LIGHTMAGENTA_EX,
        "black": Fore.BLACK, "white": Fore.WHITE, 
        "gray": Fore.LIGHTBLACK_EX, "grey": Fore.LIGHTBLACK_EX
    }

    color = fore_color.lower()
    if color in foreground_colors:
        return foreground_colors[color]
    else:
        print(f"{Fore.RED}[!] Error: {Fore.YELLOW}{color}{Fore.RED} is not a valid/supported color in this program.{Fore.RESET}")
        print(f"{Fore.GREEN}The following colors are supported:{Fore.RESET}")
        for color_key in foreground_colors.keys():
            if color_key != "gray" or color_key != "grey":
                print(f"{Fore.BLUE}{color_key}{Fore.RESET}")
            else:
                print(f"{Fore.BLUE}gray/grey{Fore.RESET}")

        exit(1)

# note: although this function is currently not in use it may be later
def validate_background_color(back_color: str) -> str:
    background_colors = {
        "blue": Back.BLUE, "light_blue": Back.LIGHTBLUE_EX, 
        "cyan": Back.CYAN, "light_cyan": Back.LIGHTCYAN_EX,
        "red": Back.RED, "light_red": Back.LIGHTRED_EX,
        "green": Back.GREEN, "light_green": Back.LIGHTGREEN_EX, 
        "yellow": Back.YELLOW, "light_yellow": Back.LIGHTYELLOW_EX,
        "magenta": Back.MAGENTA, "light_magenta": Back.LIGHTMAGENTA_EX,
        "black": Back.BLACK, "white": Back.WHITE, 
        "gray": Back.LIGHTBLACK_EX, "grey": Back.LIGHTBLACK_EX
    }

    color = back_color.lower()
    if color in background_colors:
        return background_colors[color]
    else:
        print(f"{Fore.RED}[!] Error: {Fore.YELLOW}{color}{Fore.RED} is not a valid/supported color in this program.{Fore.RESET}")
        print(f"{Fore.GREEN}The following colors are supported:{Fore.RESET}")
        for color_key in background_colors.keys():
            if color_key != "gray" or color_key != "grey":
                print(f"{Fore.BLUE}{color_key}{Fore.RESET}")
            else:
                print(f"{Fore.BLUE}gray/grey{Fore.RESET}")

        exit(1)

"""
note: 
the reason for the complex approach in this function is to avoid large amounts of color repeats, 
which was a major issue with a previous one-liner approach
"""
def paint_text(text: str, colors: list) -> str | None:
    # avoids waisting compute time with an algorithm if there is only one color provided
    if len(colors) == 1:
        return f"{validate_foreground_color(colors[0])}{text}{Fore.RESET}"

    # validates the colors and retrieves their actual color values
    colors = [validate_foreground_color(fore_color=color) for color in colors]
    # creates a list of every character in the given text
    characters = list(text)
    # keeps track of the colors list index numbers that can temporarily not be used
    banned_indexes = set()

    # len(colors) %2 == 0: even, else: odd 
    if len(colors) % 2 == 0:
        # needed colors list index(s)
        middle_index = len(colors) // 2

        # note: used to determine the random index number
        low = middle_index
        high = middle_index

        for char in range(len(text)):
            # avoids waisting compute time on non-printable characters (with the needed exceptions)
            if characters[char] == " ":
                continue
            elif characters[char].isprintable() == True or characters[char] == "\\" or characters[char] == "\'" or characters[char] == '\"':
                pass
            else:
                continue

            # note: loops until a valid index number has been selected
            while True:
                selected_index = random.randint(low, high)

                if selected_index not in banned_indexes:
                    break

            # add the color code for the current character
            characters[char] = colors[selected_index] + characters[char]

            if low != 0 and high != len(colors) - 1:
                # ban the current low and high indexes temporarily
                banned_indexes.add(low)
                banned_indexes.add(high)

                # fetch the new low and high indexes; note: center -> ends
                low -= 1
                high += 1
            else:
                # reset the low and high indexes values along with the banned_indexes set
                low = middle_index
                high = middle_index

                banned_indexes = set()

        # create the new text string
        text = "".join(characters)

        return f"{text}{Fore.RESET}"
    else:
        # needed colors list index(s)
        middle_index = ((len(colors) - 1) // 2) + 1

        # note: used to determine the random index number
        low = 0
        high = len(colors) - 1

        for char in range(len(text)):
            # avoids waisting compute time on non-printable characters (with the needed exceptions)
            if characters[char] == " ":
                continue
            elif characters[char].isprintable() == True or characters[char] == "\\" or characters[char] == "\'" or characters[char] == '\"':
                pass
            else:
                continue

            # note: loops until a valid index number has been selected
            while True:
                selected_index = random.randint(low, high)

                if selected_index not in banned_indexes:
                    break

            # add the color code for the current character
            characters[char] = colors[selected_index] + characters[char]

            if low == middle_index or high == middle_index:
                # reset the low and high indexes values along with the banned_indexes set
                low = 0
                high = len(colors) - 1

                banned_indexes = set()
            else:
                # ban the current low and high indexes temporarily
                banned_indexes.add(low)
                banned_indexes.add(high)

                # fetch the new low and high indexes; note: ends -> center
                low += 1
                high -= 1

        # create the new text string
        text = "".join(characters)

        return f"{text}{Fore.RESET}"

def input_prompt(prompt_message) -> str:
    try:
        user_choice = input(prompt_message)

        return user_choice
    except KeyboardInterrupt:
        print("\n")
        exit(0)

# [=== Classes ===] #

class Banner:
    def __init__(self):
        # elements
        self.title = str()
        self.title_bar = str()
        self.program_name = str()
        self.program_version_number = float()
        self.title_bar = str()
        self.operating_system_support_message = "This Program Supports: Linux, MacOS, and Windows"

        # element colors
        self._title_colors = list()
        self._title_bar_color = str()
        self._program_name_color = str()
        self._program_version_number_color = str()
        self._operating_system_support_message_color = str()

    # --- getter/setter properties --- #

    @property
    def title_colors(self):
        return self._title_colors
    
    @title_colors.setter
    def title_colors(self, colors: list):
        # note: the paint function will handle the color validation for the colors list
        self._title_colors = colors

    @property
    def title_bar_color(self):
        return self._title_bar_color

    @title_bar_color.setter
    def title_bar_color(self, color: str):
        self._title_bar_color = validate_foreground_color(color)

    @property
    def program_name_color(self):
        return self._program_name_color

    @program_name_color.setter
    def program_name_color(self, color: str):
        self._program_name_color = validate_foreground_color(color)

    @property
    def program_version_number_color(self):
        return self._program_version_number_color

    @program_version_number_color.setter
    def program_version_number_color(self, color: str):
        self._program_version_number_color = validate_foreground_color(color)

    @property
    def operating_system_support_message_color(self):
        return self._operating_system_support_message_color

    @operating_system_support_message_color.setter
    def operating_system_support_message_color(self, color: str):
        self._operating_system_support_message_color = validate_foreground_color(color)

class Options:
    def __init__(self):
        # elements #
        self.options = dict()
        self.previous_menu_option = True

        # element colors
        self._option_description_color = str()
        self._option_number_color = str()
        self._option_name_color = str()

        self._navigation_option_color = Fore.LIGHTBLACK_EX

    # --- getter/setter properties --- #

    @property
    def option_description_color(self):
        return self._option_description_color

    @option_description_color.setter
    def option_description_color(self, color: str):
        self._option_description_color = validate_foreground_color(color)

    @property
    def option_number_color(self):
        return self._option_number_color

    @option_number_color.setter
    def option_number_color(self, color: str):
        self._option_number_color = validate_foreground_color(color)

    @property
    def option_name_color(self):
        return self._option_name_color

    @option_name_color.setter
    def option_name_color(self, color: str):
        self._option_name_color = validate_foreground_color(color)

    @property
    def navigation_option_color(self):
        return self._navigation_option_color

    @navigation_option_color.setter
    def navigation_option_color(self, color: str):
        self._navigation_option_color = validate_foreground_color(color)

    # --- methods ---  #

    def add_option(self, option_description: str, option_number: int, option_name: str) -> None:
        # validation
        if option_number == 0:
            print(f"{Fore.RED}[!] Error: The {Fore.YELLOW}option_number 0{Fore.RED} is reserved for the exit option (automatically included).{Fore.RESET}")
            sys.exit(1)

        if option_number < 0:
            print(f"{Fore.RED}[!] Error: The chosen {Fore.YELLOW}option_number{Fore.RED} can not be negative.")
        
        if option_number in self.options.keys():
            print(f"{Fore.RED}[!] Error: The {Fore.YELLOW}option_number {option_number}{Fore.RED} is already in use.{Fore.RESET}")

        # construct and add the option to the options dictionary; note: color reset is handled when the element is added to a Menu
        option = f"{self._option_description_color}{option_description}\n{self.option_number_color}{option_number}) {self._option_name_color}{option_name}"
        
        self.options[option_number] = option

class Prompt:
    def __int__(self):
        # element(s)
        self.prompt_message = "Choose An Option From The Menu [ex: 0]: "

        # element color(s)
        self._prompt_message_color = str()

        # used to determine wether or not the user decided to color the prompt message using the module
        # note: they may have chosen not to because they wanted to use multiple colors, so instead they added the color codes themself
        self.prompt_colored = False

    # --- getter/setter properties --- #

    @property
    def prompt_message_color(self):
        return self._prompt_message_color

    @prompt_message_color.setter
    def prompt_message_color(self, color: str):
        self._prompt_message_color = validate_foreground_color(color)

        self.prompt_colored = True

class Menu:
    def __init__(self):
        # note: these strings are formated to construct menu elements (in the technical sense they are the elements)
        self._menu = ""
        self._banner = "{title}\n{title_bar_color}{title_bar}\n{program_name_color}{program_name}{program_version_number_color}v{program_version_number}\n{operating_system_support_message_color}{operating_system_support_message}{reset}"
        self._option = "{option}{reset}"

        # this variable will a hold a callable address for the input_prompt() function loaded with its parameter already
        self._prompt = None

        # used to store the option numbers for basic input validation in the run_menu method
        self._option_numbers = set()

    # --- methods ---  #

    # formally adds an element to the menu
    def _add_element(self, menu_element) -> None:
        self._menu = self._menu + f"{menu_element}\n"

    def add_banner(self, banner: Banner) -> None:
        self._add_element(menu_element=self._banner.format(
            title=paint_text(banner.title, banner.title_colors),
            title_bar_color=banner.title_bar_color,
            title_bar=banner.title_bar,
            program_name_color=banner.program_name_color,
            program_name=banner.program_name,
            program_version_number_color=banner.program_version_number_color,
            program_version_number=banner.program_version_number,
            operating_system_support_message_color=banner.operating_system_support_message_color,
            operating_system_support_message=banner.operating_system_support_message,
            reset=Fore.RESET
        ))

    def add_options(self, options: Options) -> None:
        # add the exit option
        exit_option = f"{options.navigation_option_color}0) Exit"

        self._add_element(self._option.format(
            option=exit_option,
            reset=Fore.RESET
        ))

        for option_key in options.options.keys():
            self._add_element(self._option.format(
                option=options.options[option_key],
                reset=Fore.RESET
            ))

        # add the previous menu option if necessary
        if options.previous_menu_option == True:
            previous_menu_option_number = list(options.options.keys())[-1] + 1
            previous_menu_option = f"{options.navigation_option_color}{previous_menu_option_number}) Previous Menu"
            
            self._add_element(self._option.format(
                option=previous_menu_option,
                reset=Fore.RESET
            ))

            # add the previous_menu_option with its respective option number to the options dictionary to keep a record of it
            options.options[previous_menu_option_number] = previous_menu_option

        # add the exit_option with it's respective option number to the options dictionary to keep a record of it
        options.options[0] = exit_option

        # store the option numbers to reference for basic input validation in the run_method function
        self._option_numbers = options.options.keys()

    def add_prompt(self, prompt: Prompt) -> None:
        if prompt.prompt_colored == True:
            prompt_message = f"{prompt.prompt_message_color}{prompt.prompt_message}{Fore.RESET}"
        else:
            # note: the Fore.RESET is added in case the user has forgotten to include the reset code (in the case that they manually added the color codes in their prompt_message)
            prompt_message = f"{prompt.prompt_message}{Fore.RESET}"

        # creates a callable function object with the parameter; think of it like a loaded gun ready to fire
        self._prompt = partial(input_prompt, prompt_message)

    def display_menu(self) -> None:
        print(self._menu)

    def run_menu(self) -> int:
        print(self._menu)

        while True:
            user_choice = self._prompt()

            try:
                user_choice = int(user_choice)

                if user_choice == 0:
                    exit(0)

                if user_choice in self._option_numbers:
                    clear_terminal()

                    return user_choice
                else:
                    print(f"{Fore.RED}Invalid Option!{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Invalid Option!{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}Invalid Option!{Fore.RESET}")

class Menataur:
    pass
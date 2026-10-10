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
The Menataur class organizes the menu components and uses a navigation algorithm to allow 
users to move between them.

note: 
When reading the menu navigation algorithm code in this program (split between Menu and Menataur), think about a Binary Tree
and it will begin to make a lot more sense. I believe this is the simplest way to make sb ense
of the navigation algorithm.

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

prompt.prompt_message_color = "light_magenta"
prompt.prompt_message = "Select an option: "

# create and run the menu
menu = Menu()

menu.name = "main"
menu.main_menu = True

menu.add_banner(banner)
menu.add_options(options)
menu.add_prompt(prompt)

menu.run()

# you can only simply display it (excludes the input prompt)
menu.display()
"""

# [=== Imports ===] #

from functools import partial
import subprocess
import random
import sys

# [=== Global Variables ===]

# used to ensure the user does not give two or more Menu's the same name
_used_menu_name: list[str] = list()

# note: this dictionary is global so that users are able to add their own custom colors to use
foreground_colors = {
"blue": "\033[34m", "light_blue": "\033[94m",
"cyan": "\033[36m", "light_cyan": "\033[96m",
"red": "\033[31m", "light_red": "\033[91m",
"green": "\033[32m", "light_green": "\033[92m",
"yellow": "\033[33m", "light_yellow": "\033[93m",
"magenta": "\033[35m", "light_magenta": "\033[95m",
"black": "\033[30m", "white": "\033[37m",
"gray": "\033[90m", "grey": "\033[90m"
}

# for resetting the foreground color
fore_reset = "\033[0m"

# [=== Functions ===] #

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
        print(f"{Fore.GREEN}The following colors are supported:{fore_reset}")
        for color_key in foreground_colors.keys():
            if color_key != "gray" or color_key != "grey":
                print(f"{foreground_colors[color_key]}{color_key}{fore_reset}")
            else:
                print(f"{foreground_colors[color_key]}gray/grey{fore_reset}")

        exit(1)

"""
note: 
the reason for the complex approach in this function is to avoid large amounts of color repeats, 
which was a major issue with a previous one-liner approach
"""
def paint_text(text: str, colors: list) -> str:
    # avoids waisting compute time with an algorithm if there is only one color provided
    if len(colors) == 1:
        return f"{validate_foreground_color(colors[0])}{text}{fore_reset}"

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

        return f"{text}{fore_reset}"
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

        return f"{text}{fore_reset}"

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
        self._title_colors: list[str] = list()
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
        self.options: dict[int, str] = dict()

        # element colors
        self._option_description_color = str()
        self._option_number_color = str()
        self._option_name_color = str()

        self._navigation_option_color = foreground_colors["gray"]

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
            print(f"{foreground_colors["red"]}[!] Error: The {foreground_colors["yellow"]}option_number 0{foreground_colors["red"]} is reserved for the exit option (automatically included).{fore_reset}")
            sys.exit(1)

        if option_number < 0:
            print(f"{foreground_colors["red"]}[!] Error: The chosen {foreground_colors["yellow"]}option_number{foreground_colors["red"]} can not be negative.")
        
        if option_number in self.options.keys():
            print(f"{foreground_colors["red"]}[!] Error: The {foreground_colors["yellow"]}option_number {option_number}{foreground_colors["red"]} is already in use.{fore_reset}")

        if self.option_description_color != str() and self.option_number_color != str() and self.option_description_color != str():
            # construct and add the option to the options dictionary; note: color reset is handled when the element is added to a Menu
            option = f"{self._option_description_color}{option_description}{fore_reset}\n{self._option_number_color}{option_number}) {fore_reset}{self._option_name_color}{option_name}"

            self.options[option_number] = option
        else:
            print(f"{foreground_colors["red"]}[!] Error: You must define the {foreground_colors["yellow"]}Options object's colors{foreground_colors["red"]} before setting the options, otherwise the Options object's colors won't render.{fore_reset}")
            exit(1)

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
        self._menu = str()
        self._banner = "{title}\n{title_bar_color}{title_bar}\n{program_name_color}{program_name} {program_version_number_color}v{program_version_number}\n{operating_system_support_message_color}{operating_system_support_message}\n{reset}"
        self._option = "{option}{reset}"

        # this variable will a hold the callable address for the input_prompt() functions loaded with their parameter already
        self._prompts: list[str] = list()

        # used to make it easier to sort through the final Menataur (menu interface) data
        self._name = str()
        # used to determine wether or not this is a/the main menu
        self.main_menu = False
        # used to determine wether or not this is the final menu in a menu path
        self._final_menu = False
        # used to store the option numbers for basic input validation in the run_menu method
        self._option_numbers: set[int] = set()
        # used to store the Option to Menu mappings - required if the user want's to use this Menu in a Menataur
        self._datamap: dict[int, Menu | str] = dict()

    # --- getter/setter properties --- #

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, menu_name: str):
        if menu_name in _used_menu_name:
            print(f"{foreground_colors["red"]}[!] Error: Every Menu must be assigned a unique {foreground_colors["yellow"]}name{foreground_colors["red"]}.{fore_reset}")
            exit(1)
        
        _used_menu_name.append(menu_name)

        self._name = menu_name

    @property
    def final_menu(self):
        return self._final_menu

    @final_menu.setter
    def final_menu(self, value: bool):
        if value == True:
            # used to create a special data map for the final menu
            _final_menu_datamap: dict[int, str] = dict()
            # used to know when to stop looping; note: 1 is not subtracted for previous menu because of the way the range() function works
            _last_option = max(self._option_numbers)

            _final_menu_datamap[0] = "exit"

            for opt in range(1, _last_option):
                _final_menu_datamap[opt] = "final_menu"

            _final_menu_datamap[_last_option] = "previous_menu"

            self._datamap = _final_menu_datamap
        
        # set the _final_menu tracker variable to the user given bool (True or False)
        self._final_menu = value

    @property
    def datamap(self):
        return self._datamap

    @datamap.setter
    def datamap(self, map: dict):
        # ensure this is not a final menu because final Menus do not need a user configured datamap
        if self.final_menu == True:
            print(f"{foreground_colors["red"]}[!] Error: This is a {foreground_colors["yellow"]}Final Menu{foreground_colors["red"]}, it should not have a datamap.{fore_reset}")
            exit(1)

        # add the exit and previous menu (if applicable) options 
        map[0] = "exit"

        if self.main_menu != True:
            map[(max(self._option_numbers)) + 1] = "previous_menu"

        self._datamap = map

        # ensure the user has provided map keys that match the option numbers and store the map if so
        if map.keys() != self._datamap.keys():
            print(f"{foreground_colors["red"]}[!] Error: The {foreground_colors["yellow"]}map keys{foreground_colors["red"]} do not match the {foreground_colors["yellow"]}option numbers{foreground_colors["red"]}.{fore_reset}")
            print(map.keys())
            print(self._datamap.keys())
            exit(1)

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
            reset=fore_reset
        ))

    def add_options(self, options: Options) -> None:
        # add the exit option
        exit_option = f"{options.navigation_option_color}0) Exit"

        self._add_element(self._option.format(
            option=exit_option,
            reset=fore_reset
        ))

        for option_key in options.options.keys():
            self._add_element(self._option.format(
                option=options.options[option_key],
                reset=fore_reset
            ))

        # add the previous menu option if necessary
        if self.main_menu != True:
            previous_menu_option_number = list(options.options.keys())[-1] + 1
            previous_menu_option = f"{options.navigation_option_color}{previous_menu_option_number}) Previous Menu"

            self._add_element(self._option.format(
                option=previous_menu_option,
                reset=fore_reset
            ))

            # add the previous_menu_option with its respective option number to the options dictionary to keep a record of it
            options.options[previous_menu_option_number] = previous_menu_option

        # add the exit_option with it's respective option number to the options dictionary to keep a record of it
        options.options[0] = exit_option

        # store the option numbers to reference for basic input validation in the run_method function
        self._option_numbers = options.options.keys()

    def add_prompt(self, prompt: Prompt) -> None:
        if prompt.prompt_colored == True:
            prompt_message = f"{prompt.prompt_message_color}{prompt.prompt_message}{fore_reset}"
        else:
            # note: the fore_reset is added in case the user has forgotten to include the reset code (in the case that they manually added the color codes in their prompt_message)
            prompt_message = f"{prompt.prompt_message}{fore_reset}"

        # creates a callable function object with the parameter; think of it like a loaded gun ready to fire
        prompt = partial(input_prompt, prompt_message)

        # appends the callable prompt function object to the _prompts list
        self._prompts.append(prompt)


    def add_prompts(self, prompts: list[Prompt]) -> None:
        for prompt in prompts:
            if prompt.prompt_colored == True:
                prompt_message = f"{prompt.prompt_message_color}{prompt.prompt_message}{fore_reset}"
            else:
                # note: the fore_reset is added in case the user has forgotten to include the reset code (in the case that they manually added the color codes in their prompt_message)
                prompt_message = f"{prompt.prompt_message}{fore_reset}"

            # creates a callable function object with the parameter; think of it like a loaded gun ready to fire
            prompt = partial(input_prompt, prompt_message)

            # appends the callable prompt function object to the _prompts list
            self._prompts.append(prompt)

    def display(self) -> None:
        print(self._menu)

    def run(self) -> list:
        user_choices: list = list()
        print(self._menu)

        if self.name == str():
            print(f"{foreground_colors["red"]}[!] Error: Every Menu must be assigned a unique{foreground_colors["yellow"]}name{foreground_colors["red"]}.{fore_reset}")
            exit(1)

        try:
            # run the first prompt (Menu option prompt) and validate the input
            while True:
                user_choice = self._prompts[0]()
                try:
                    user_choice = int(user_choice)

                    if user_choice == 0:
                        exit(0)
                    elif user_choice == max(self._option_numbers):
                        user_choices.append(user_choice)

                        return user_choices
                    elif user_choice in self._option_numbers:
                        user_choices.append(user_choice)
                        break
                    else:
                        print(f"{foreground_colors["red"]}Invalid Option!{fore_reset}")
                except ValueError:
                    print(f"{foreground_colors["red"]}Invalid Option!{fore_reset}")
                except IndexError:
                    print(f"{foreground_colors["red"]}Invalid Option!{fore_reset}")
                except Exception as e:
                    print(e)
                    exit(1)

            if len(self._prompts) > 1:
                for prompt in self._prompts[1:]:
                    user_choice = prompt()
                    user_choices.append(user_choice)

        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(f"{foreground_colors["red"]}[!] Error: Unknown.{fore_reset}")
            print(e)
            exit(1)

        clear_terminal()

        return user_choices

class Menataur:
    def __init__(self):
        # stores the starting position of the Menataur (menu interface)
        self._start_menu = None

    @property
    def start_menu(self):
        return self._start_menu

    @start_menu.setter
    def start_menu(self, menu: Menu):
        if menu.main_menu == True:
            self._start_menu = menu
        else:
            print(f"{foreground_colors["red"]}[!] Error: The {foreground_colors["yellow"]}start_menu{foreground_colors["red"]} must be a {foreground_colors["yellow"]}main_menu{foreground_colors["red"]}.{fore_reset}")
            print(f"{foreground_colors["blue"]}[?] Help: If you would like to use this {foreground_colors["yellow"]}menu{foreground_colors["blue"]} as your start_menu, set {foreground_colors["yellow"]}main_menu=True{foreground_colors["blue"]}.{fore_reset}")
            exit(1)

    def run(self) -> list[dict[str, list]]:
        current_menu: Menu = self.start_menu
        previous_menu: Menu = Menu()
        user_choices: list[dict[str, list]] = list()

        if self._start_menu == None:
            print(f"{foreground_colors["red"]}[!] Error: You must set a {foreground_colors["yellow"]}start_menu{foreground_colors["red"]}.{fore_reset}")

        while True:
            menu_output = current_menu.run()

            next_menu = current_menu.datamap[menu_output[0]]

            # next menu is the problem resulting in the overpop of user choices
            match next_menu:
                case "final_menu":
                    clear_terminal()

                    if menu_output[0] == max(current_menu.datamap.keys()) and current_menu != self.start_menu:
                        if len(user_choices) > 0:
                            user_choices.pop()

                        continue
                    else:
                        menu_user_choices_map = {current_menu.name: menu_output}
                        user_choices.append(menu_user_choices_map)

                    return user_choices
                case _:
                    clear_terminal()
                    
                    if next_menu.main_menu != True:
                        previous_menu = current_menu
                        next_menu.datamap[max(next_menu.datamap.keys())] = previous_menu

                    if menu_output[0] == max(current_menu.datamap.keys()) and current_menu != self.start_menu:
                        if len(user_choices) > 0:
                            user_choices.pop()
                    else:
                        menu_user_choices_map = {current_menu.name: menu_output}
                        user_choices.append(menu_user_choices_map)
                    
                    current_menu = next_menu

                    continue

# https://rnsaffn.com/poison2/
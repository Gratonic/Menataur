# [=== Imports ===] #

# Copyright (c) 2013-2023, Anthony Sottile
from colorama import Fore, Back
import json

# [=== Functionality ===] #

# used to validate colors and retrieve their respective colorama color objects
class Palettaur():
    def __init__(self):
        # colors supported by the module - Palettaur
        self._supported_colors = [
            "blue", "light_blue", 
            "cyan", "light_cyan", 
            "red", "light_red", 
            "green", "light_green", 
            "yellow", "light_yellow", 
            "magenta", "light_magenta", 
            "white", "gray", "black"
        ]
        # supported foreground colors and their colorama color objects
        self._foreground_colors = {
            "blue": Fore.BLUE, "light_blue": Fore.CYAN, 
            "cyan": Fore.CYAN, "light_cyan": Fore.CYAN, 
            "red": Fore.RED, "light_red": Fore.RED, 
            "green": Fore.GREEN, "light_green": Fore.GREEN, 
            "yellow": Fore.YELLOW, "light_yellow": Fore.YELLOW, 
            "magenta": Fore.MAGENTA, "light_magenta": Fore.MAGENTA, 
            "white": Fore.WHITE, "gray": Fore.LIGHTBLACK_EX, "black": Fore.BLACK
        }
        # supported background colors and their colorama color objects
        self.background_colors = {
            "blue": Back.BLUE, "light_blue": Back.CYAN, 
            "cyan": Back.CYAN, "light_cyan": Back.CYAN, 
            "red": Back.RED, "light_red": Back.RED, 
            "green": Back.GREEN, "light_green": Back.GREEN, 
            "yellow": Back.YELLOW, "light_yellow": Back.YELLOW,
            "magenta": Back.MAGENTA, "light_magenta": Back.MAGENTA, 
            "white": Back.WHITE, "gray": Back.LIGHTBLACK_EX, "black": Back.BLACK
        }

    # :: Main Functionality :: #

    # validates and retrieves the colorama color object of a foreground color
    def validate_foreground_color(self, color: str) -> object:
        color = color.lower()
        if color in self._foreground_colors:
            return self._foreground_colors[color]
        else:
            print(f"{Fore.RED}[!] Error: The color you have specified is invalid or unsupported.{Fore.RESET}")
            print("\n")
            print(f"{Fore.YELLOW}[*] The following foreground colors are supported...{Fore.RESET}")
            for color_name in self._foreground_colors.keys():
                print(f"{Fore.LIGHTCYAN_EX}{color_name}{Fore.RESET}")
            exit()
    # validates and retrieves the colorama color object of a background color
    def validate_background_color(self, color: str) -> object:
        color = color.lower()
        if color in self.background_colors:
            return self.background_colors[color]
        else:
            print(f"{Fore.RED}[!] Error: The color you have specified is invalid or unsupported.{Fore.RESET}")
            print("\n")
            print(f"{Fore.YELLOW}[*] The following background colors are supported...{Fore.RESET}")
            for color_name in self.background_colors.keys():
                print(f"{Fore.LIGHTCYAN_EX}{color_name}{Fore.RESET}")
            exit()

    # :; Helpful/Debug Functionality :: #

    # lists the colors supported by the module
    def list_supported_colors(self):
        print(f"{Fore.YELLOW}[*] Supported Colors: \n{Fore.RESET}")
        for index, color in enumerate(self._supported_colors, start=1):
            print(f"{Fore.BLUE}{index}{Fore.YELLOW}) {Fore.LIGHTCYAN_EX}{color}{Fore.RESET}")

# used to construct new individual user interface menus
class Menu():
    def __init__(self):
        # placeholder for the menu
        self._menu = ""
        # format string placeholders for the menu elements
        self._header = "{ascii_title}\n{title_bar}\n{program_info_message}\n{os_support_message}{foreground_reset}"
        self._description = "{description}{foreground_reset}"
        self._option = "{menu_option_number}{seperator} {menu_option}{foreground_reset}"

        # placeholders for input and input_message - different compared to the others
        self._input = ""
        self._input_message = "{input_message}{foreground_reset}"

    # :: Main Functionality :: #

    # constructs a menu element and adds it to the menu
    def _construct(self, element: str) -> None:
        self._menu = f"{self._menu}{element}\n"
    
    # configures the input_message for the get_user_input() function
    def _configure_input_message(self, message: str):
        self._input_message = message
    
    # gets the user input using the _input_message and returns the user's input
    def get_user_input(self):
        if self._input_message != "{input_message}{foreground_reset}":
            try:
                return input(self._input_message)
            except KeyboardInterrupt:
                print("\n")
                pass
            except Exception as e:
                print(e)
        else:
            print(f"{Fore.RED}[!] Error: Menu input_message needs to be set.{Fore.RESET}")
    
    # displays the menu in its current state
    def display_menu(self):
        print(self._menu)
    
    # builds a menu header element and adds it to the menu using the internal construct function
    def add_header(self, ascii_title_colors: list, ascii_title: str, title_bar_color: str, title_bar: str, program_name_color: str, program_name: str, program_version_color: str, program_version: float, os_support_foreground_color: str, os_support_background_color: str, os_support_message: str, supported_operating_systems_info: list) -> None:
        # creates an instance of Palettaur for foreground and background color validation
        palettaur = Palettaur()

        # validates the ascii_title_colors using Palettaur
        ascii_title_colors = [palettaur.validate_foreground_color(color) for color in ascii_title_colors]
        # constructs the colorful and complete title using the ascii_title and ascii_title_colors
        title = ''.join(ascii_title_colors[char % len(ascii_title_colors)] + ascii_title[char] for char in range(len(ascii_title)))
        # validates the title_bar_color using Palettaur
        title_bar_color = palettaur.validate_foreground_color(title_bar_color)
        # constructs the colorful and complete title bar using the title_bar and title_bar_color
        title_bar = f"{title_bar_color}{title_bar}"
        # validates the program_name_color and program_version_color using Palettaur
        program_name_color = palettaur.validate_foreground_color(program_name_color)
        program_version_color = palettaur.validate_foreground_color(program_version_color)
        # constructs the colorful and complete program_info_message using the program_name_color, program_name, program_version_color, program_version
        program_info_message = f"{program_name_color}{program_name} {program_version_color}v{program_version}"
        # validates the os_support_foreground_color and os_support_background_color using Palettaur
        os_support_foreground_color = palettaur.validate_foreground_color(os_support_foreground_color)
        os_support_background_color = palettaur.validate_background_color(os_support_background_color)
        # constructs the colorful and complete os_support_message using the os_support_foreground_color, os_support_background_color, os_support_message, and supported_operating_systems_info
        os_support_message = f"{os_support_foreground_color}{os_support_message}"
        for os in supported_operating_systems_info:
            if os != supported_operating_systems_info[-1]:
                os_support_message = os_support_message + f" {os_support_background_color}{os}{Back.RESET},"
            else:
                os_support_message = os_support_message + f" {os_support_background_color}{os}{Back.RESET}"


        self._construct(self._header.format(
            ascii_title=title,
            title_bar=title_bar,
            program_info_message=program_info_message,
            os_support_message=os_support_message,
            foreground_reset=Fore.RESET
        ))

    # builds a menu description element and adds it to the menu using the internal construct function
    def add_description(self, description_color: str, description: str) -> None:
        # creates an instance of Palettaur for foreground and background color validation
        palettaur = Palettaur()

        # validates the description_color using Palettaur
        description_color = palettaur.validate_foreground_color(description_color)
        # constructs the colorful and complete description using the description_color and description
        description = f"{description_color}{description}"
        
        self._construct(self._description.format(
            description=description,
            foreground_reset=Fore.RESET
        ))

    # builds a menu option element and adds it to the menu using the internal construct function
    def add_option(self, menu_option_number_color: str, menu_option_number: int, seperator_color: str, seperator: str, menu_option_color: str, menu_option: str) -> None:
        # creates an instance of Palettaur for foreground and background color validation
        palettaur = Palettaur()

        # validates the menu_option_number_color using Palettaur
        menu_option_number_color = palettaur.validate_foreground_color(menu_option_number_color)
        # constructs the colorful and complete menu_option_number using the menu_option_number_color and menu_option_number
        menu_option_number = f"{menu_option_number_color}{menu_option_number}"
        # validates the seperator_color using Palettaur
        seperator_color = palettaur.validate_foreground_color(seperator_color)
        # constructs the colorful and complete seperator using the seperator_color and seperator
        seperator = f"{seperator_color}{seperator}"
        # validates the menu_option_color using Palettaur
        menu_option_color = palettaur.validate_foreground_color(menu_option_color)
        # constructs the colorful and complete menu_option using the menu_option_color and menu_option
        menu_option = f"{menu_option_color}{menu_option}"

        self._construct(self._option.format(
            menu_option_number=menu_option_number,
            seperator=seperator,
            menu_option=menu_option,
            foreground_reset=Fore.RESET
        ))

    # creates and sets the input message of the menu input field using the internal construct function
    def set_input_message(self, input_message_color: str, input_message: str) -> None:
        # creates an instance of Palettaur for foreground and background color validation
        palettaur = Palettaur()

        # validates the input_message_color using Palettaur
        input_message_color = palettaur.validate_foreground_color(input_message_color)
        # constructs the colorful and complete input_message using the input_message_color and input_message
        input_message = f"{input_message_color}{input_message}"
        
        self._configure_input_message(self._input_message.format(
            input_message=input_message,
            foreground_reset=Fore.RESET
        ))
    
    # :: Special Functionality :: #

    # calls the menu in its current state with its input field (if it has been configured)
    def call_menu(self):
        print(self._menu)
        self.get_user_input()

class Menu_Stack():
    def __init__(self):
        pass

class Menu_Interface():
    def __init__(self):
        pass

class Menataur():
    def __init__(self):
        pass
# Class Structure

## Menataur

Menataur.menu_from_json(json_file: str)
Menataur.menu_from_params(params)
Menataur.menu_stack(menus: dict)
Menataur.menu_interface(menu_stacks: dict)

Menataur.display_menu(menu: Menu, store_as_json=False)
Menataur.list_menu_contents(menu: Menu)
Menataur.list_menu_stack(menu_stack: Menu_Stack)
Menataur.list_menu_interface(menu_interface: Menu_Interface)
Menataur.list_menu_interface_with_menu_stacks(menu_interface: Menu_Interface)

## Menataur Internal Classes

Menu: used to create menu
Menu_Stack: used to create menu stack
Menu_Interface: used to create menu interface

## Special Internal Classes

Palettaur: used to validate colors and retrieve their color object using colorama - for Menu class
Debug: used for various debugging purposes - for all classes

# Functionality To Keep From 1st Menataur Version

## Validates the colors provided by the user - Modify
def validate_color(color: str) -> str:
    color = color.lower()
    if color in supported_colors:
        return supported_colors[color]
    else:
        print(f"{red}[!] Minotaur Error: {light_red}One or more color(s) is/are not valid or is/are unsupported.{reset}")
        print(f"{green}The following colors are supported:{reset}")
        for color_str in supported_colors.keys():
            print(f"{blue}{color_str}{reset}")
        raise ValueError("Invalid color provided.")

## Menu Builder Class - Modify
class Menu():
    def __init__(self):
        self._placeholder = ""
        self._header = "{ascii_art_title}\n{title_bar}\n{program_version_color}{small_title} v{program_version_num}\n{os_support_message}{reset}"
        self._body = "{accent_color}{menu_option_number}) {menu_option_color}{menu_option}{reset}"
        self._paragraph = "{text_color}{text}{reset}"
        self._footer = "{text_color}{text}{reset}"
    # Formally adds an element to the menu interface
    def _include(self, element):
        self._placeholder = self._placeholder + f"{element}\n"
    # Adds a header element (title, os support info, etc.) to the menu interface
    def add_header(self, ascii_art_title: str, small_title: str, title_colors: list, title_bar_width: int, title_bar: list, program_version_color: str, program_version_num: str, os_support_message_color: str, os_support_highlight_color: str, os_support_color: str, os_support_info: list) -> None:
        # Validates the colors in the title colors list and gets the real color if they are valid
        validated_title_colors = [validate_color(color) for color in title_colors]
        # Creates a colorful title using the provided ascii_art_title and title colors
        colorful_title = ''.join(validated_title_colors[char % len(validated_title_colors)] + ascii_art_title[char] for char in range(len(ascii_art_title)))
        # Creates the title bar using the title bar width
        title_bar = f"{title_bar[0] * (title_bar_width - 1)}{title_bar[1]}"
        # Validates the os_support_color
        os_support_color = validate_color(os_support_color)
        # Validates the os_support_highlight_color and sets its value
        os_support_highlight_color = validate_highlight_color(os_support_highlight_color)
        # Creates the os support message using the os support info list, os support highlight color, and os_support_color
        os_support_message = f"{os_support_color}This Program Supports:"
        
        for os in os_support_info:
            if os != os_support_info[-1]:
                os_support_message = os_support_message + f" {os_support_highlight_color}{os}{highlight_reset},"
            else:
                os_support_message = os_support_message + f" {os_support_highlight_color}{os}{highlight_reset}"
        
        self._include(self._header.format(
            ascii_art_title=colorful_title,
            small_title=small_title,
            title_bar=title_bar,
            program_version_color=validate_color(program_version_color),
            program_version_num=program_version_num,
            os_support_message=os_support_message,
            reset=reset
        ))
    # Adds a body element (menu option) to the menu interface
    def add_body(self, accent_color: str, menu_option_number: int, menu_option_color: str, menu_option: str) -> None:
        self._include(self._body.format(
            accent_color=validate_color(accent_color),
            menu_option_number=menu_option_number,
            menu_option_color=validate_color(menu_option_color),
            menu_option=menu_option,
            reset=reset
        ))
    # Adds a paragraph (description) to the menu interface
    def add_paragraph(self, text_color: str, text: str, title_width=5) -> None:
        self._include(self._paragraph.format(
            text_color=validate_color(text_color),
            text=text,
            reset=reset
        ))
    # Adds a footer element (thank you or warning message) to the menu interface
    def add_footer(self, text_color: str, text: str, title_width=5) -> None:
        if not isinstance(title_width, int):
            print(f"{red}[!] Minotaur Error: {yellow}title_width {light_red}must be type: {yellow}int{reset}")
            raise ValueError("title_width must be an integer.")
        
        text = f"{' ' * (title_width // 2)}{text}{' ' * (title_width // 2)}"
        self._include(self._paragraph.format(
            text_color=validate_color(text_color),
            text=text,
            reset=reset
        ))
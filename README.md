# :: Author Information and Program Details :: #

Module Name: Menataur (Menataur/menataur.py) | 
Author: Gratonic (https://github.com/Gratonic) | 
Contributing Author: FailurePoint (https://github.com/FailurePoint) | 
Written In: Python 3.10.12 | 
Dependencie(s): colorama | 
Last Modified: February 9th, 2025

# :: Description :: #

This Module is used to build a menu interface with an ASCII Art Title.
The add_header() function is used to build the header portion of a menu (ASCII Art Title, OS Support Information, etc.). The add_body() function is used to
add a menu option to the menu. The add_paragraph() function is used to add a description to the menu. The add_footer()
function is used to add a sentence/description at a desired location on the menu (likely the bottom) with padding. The color
validation function are used to validate the colors passed to the function by checking the given color or colors against a 
dictionary of the colors supported by the program and then set the color to the chosen colors actual value. When add_header(),
add_body(), add_paragraph(), and_footer() are called, the parameters are used to format place holder strings which are then added
to the _placeholder format string (the actual menu) with the _include() function, which is responsible for tacking the pieces
of the menu onto the menu. Think of this program like a lego project, each piece of the menu is like a lego structure and the
pieces of that lego structure are the configuration settings for that lego structure, and think of the _include() function as the
function that attaches that lego structure to the lego project. Alternatively, you can think of it sort of like a webpage written
in just HTML and CSS.

# :: Example Usage :: #

```python
import menataur
menu = menataur.Menataur()
menu.add_header(
    ascii_art_title=ascii_art_title,
    small_title=small_title,
    title_colors=title_colors,
    title_bar=title_bar,
    program_version_color=program_version_color,
    program_version_num=program_version_num,
    os_support_message_color=os_support_message_color,
    os_support_highlight_color=os_support_highlight_color,
    os_support_color=os_support_color,
    os_support_info=os_support_info
)
menu.add_paragraph(text_color="grey", text="Have some fun at a party")
menu.add_body(accent_color="magenta", menu_option_number=1, menu_option_color="light_cyan", menu_option="Party")
menu.add_paragraph(text_color="grey", text="Drink way too much")
menu.add_body(accent_color="magenta", menu_option_number=2, menu_option_color="light_cyan", menu_option="Get Drunk")
menu.add_paragraph(text_color="grey", text="Go to bed and sleep")
menu.add_body(accent_color="magenta", menu_option_number=3, menu_option_color="light_cyan", menu_option="Sleep")
menu.add_paragraph(text_color="grey", text="All three")
menu.add_body(accent_color="magenta", menu_option_number=4, menu_option_color="light_cyan", menu_option="The Works")
menu.add_footer(text_color="light_yellow", text="Thank you for using Minotaur!")
menu.execute()
```

NOTE: multipule menu obects can be created and used at once, ie: `main_menu = menataur.Menataur()`, `pageone = menataur.Menataur()`
, `pagetwo = menataur.Menataur()`


# Breakdown

## Imports the module
import menataur

## Creates an instance of Menataur (the menu class)
menu = menataur.Menataur()

## Add the header to the menu
menu.add_header(
    ascii_art_title=ascii_art_title,
    small_title=small_title,
    title_colors=title_colors,
    title_bar=title_bar,
    program_version_color=program_version_color,
    program_version_num=program_version_num,
    os_support_message_color=os_support_message_color,
    os_support_highlight_color=os_support_highlight_color,
    os_support_color=os_support_color,
    os_support_info=os_support_info
)

## Add body elements (menu options)
menu.add_paragraph(text_color="grey", text="Have some fun at a party")
menu.add_body(accent_color="magenta", menu_option_number=1, menu_option_color="light_cyan", menu_option="Party")
menu.add_paragraph(text_color="grey", text="Drink way too much")
menu.add_body(accent_color="magenta", menu_option_number=2, menu_option_color="light_cyan", menu_option="Get Drunk")
menu.add_paragraph(text_color="grey", text="Go to bed and sleep")
menu.add_body(accent_color="magenta", menu_option_number=3, menu_option_color="light_cyan", menu_option="Sleep")
menu.add_paragraph(text_color="grey", text="All three")
menu.add_body(accent_color="magenta", menu_option_number=4, menu_option_color="light_cyan", menu_option="The Works")

## Add a footer (thank you message)
menu.add_footer(text_color="light_yellow", text="Thank you for using Menataur!")

## Completes and calls the menu
menu.execute()

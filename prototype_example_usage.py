# Imports the module
import menataur_prototype

# Creates an instance of Minotaur (the menu class)
menu = menataur_prototype.Menataur()

# Define the elements for the menu
ascii_art_title = r"""
 _______ _________ _        _______ _________ _______           _______ 
(       )\__   __/( (    /|(  ___  )\__   __/(  ___  )|\     /|(  ____ )
| () () |   ) (   |  \  ( || (   ) |   ) (   | (   ) || )   ( || (    )|
| || || |   | |   |   \ | || |   | |   | |   | (___) || |   | || (____)|
| |(_)| |   | |   | (\ \) || |   | |   | |   |  ___  || |   | ||     __)
| |   | |   | |   | | \   || |   | |   | |   | (   ) || |   | || (\ (   
| )   ( |___) (___| )  \  || (___) |   | |   | )   ( || (___) || ) \ \__
|/     \|\_______/|/    )_)(_______)   )_(   |/     \|(_______)|/   \__/
"""
small_title = "Minotaur"
title_colors = ["red", "white", "blue"]
title_bar_width = 75
title_bar = ["_", "/"]
program_version_color = "green"
program_version_num = "1.0"
os_support_message_color = "yellow"
os_support_highlight_color = "light_green"
os_support_color = "light_cyan"
os_support_info = ["Windows", "Linux", "MacOS"]

# Add the header to the menu
menu.add_header(
    ascii_art_title=ascii_art_title,
    small_title=small_title,
    title_colors=title_colors,
    title_bar_width=title_bar_width,
    title_bar=title_bar,
    program_version_color=program_version_color,
    program_version_num=program_version_num,
    os_support_message_color=os_support_message_color,
    os_support_highlight_color=os_support_highlight_color,
    os_support_color=os_support_color,
    os_support_info=os_support_info
)

# Add body elements (menu options)
menu.add_paragraph(text_color="grey", text="Have some fun at a party")
menu.add_body(accent_color="magenta", menu_option_number=1, menu_option_color="light_cyan", menu_option="Party")
menu.add_paragraph(text_color="grey", text="Drink way too much")
menu.add_body(accent_color="magenta", menu_option_number=2, menu_option_color="light_cyan", menu_option="Get Drunk")
menu.add_paragraph(text_color="grey", text="Go to bed and sleep")
menu.add_body(accent_color="magenta", menu_option_number=3, menu_option_color="light_cyan", menu_option="Sleep")
menu.add_paragraph(text_color="grey", text="All three")
menu.add_body(accent_color="magenta", menu_option_number=4, menu_option_color="light_cyan", menu_option="The Works")

# Add a footer (thank you message)
menu.add_footer(text_color="light_yellow", text="Thank you for using Minotaur!")

# Completes and calls the menu
choice = menu.execute(prompt_color="blue", input_prompt_message="Please choose an option from the menu [ex: 2]: ")

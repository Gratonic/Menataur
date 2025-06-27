# Menataur

## Module Details

- **Module Name:** Menataur (menataur_v1.0.py)  
- **Author:** Gratonic (https://github.com/Gratonic)
- **Contributing Author:** FailurePoint (https://github.com/FailurePoint)
- **Written In:** Python 3.12.3 
- **Dependencies:** colorama, json 
- **Last Modified:** 6/26/2025 

## Overview

Menataur is a Python module designed to create colorful and interactive menus in the terminal. It allows users to build menus from parameters or JSON files, providing a flexible way to present options and gather user input.

## Features

- **Colorful Menus:** Customize the appearance of menus with various foreground and background colors.
- **Dynamic Input Handling:** Validate user input to ensure it meets specified criteria.
- **Menu Stacks:** Create and manage multiple menus easily.
- **JSON Support:** Load menu configurations from JSON files for easy customization.

## Installation

To install the required dependencies, run:

```bash

pip install -r requirements.txt

```

```python

from menataur_v1.0 import Menataur

# Create an instance of Menataur
menataur = Menataur()

# Define your menu parameters
ascii_title_colors = ["blue", "light_blue"]
ascii_title = "Welcome to Menataur"
title_bar_color = "cyan"
title_bar = "===================="
program_name = "Menataur"
program_version = 1.0
os_support_message = "Supports Windows, macOS, Linux"
supported_os = ["Windows", "macOS", "Linux"]
description_colors = {0: "light_green"}
descriptions = {0: "Choose an option from the menu below:"}
option_colors = {0: "light_yellow"}
options = {0: "Exit"}
call_functions = {0: exit} # NOTE: exit is a function object 
input_message_color = "white"
input_message = "Please enter your choice:"

# Build the menu from params
menu = menataur.menu_from_params(
    ascii_title_colors, ascii_title, title_bar_color, title_bar,
    "green", "light_green", program_name, program_version,
    "yellow", "black", os_support_message, supported_os,
    description_colors, descriptions, "light_red", ":", option_colors, options, call_functions,
    input_message_color, input_message
)

# Build the menu from json
menu = menataur.menu_from_json("Example_Menus/dessert.json", call_functions) # call_functions is a dict, exactly like the one above

# Call the menu
user_choice = menu.call_menu()

```

# Example JSON Structure

```json
{
    "header": {
        "ascii_title_colors": ["blue", "light_blue"],
        "ascii_title": "menataur_ascii_title.txt",
        "title_bar_color": "cyan",
        "title_bar": "====================",
        "program_name_color": "green",
        "program_version_color": "light_green",
        "program_name": "Dessert Menu",
        "program_version": 1.0,
        "os_support_foreground_color": "yellow",
        "os_support_background_color": "black",
        "os_support_message": "Supports Windows, macOS, Linux",
        "supported_operating_systems": ["Windows", "macOS", "Linux"]
    },
    "descriptions": {
        "0": {
            "description_color": "light_green",
            "description": "Choose your favorite dessert:"
        }
    },
    "options": {
        "0": {
            "option_number_color": "light_yellow",
            "seperator_color": "light_red",
            "seperator": ":",
            "option_color": "light_yellow",
            "option": "Chocolate Cake"
        }
    },
    "input_field": {
        "input_message_color": "white",
        "input_message": "Please enter your choice:"
    }
}

```
import json
from typing import Dict
from os import path, get_terminal_size
from time import sleep 
from random import randrange
import textwrap as tr

DATA_SOURCE = path.abspath('useless_machine/data/useless_data.json')
FAREWELL_FILE = path.abspath('useless_machine/data/farewell.json')
LINE_LENGTH = 80
REVERSE_COUNTER = 3
TERM_WIDTH, TERM_LINES = get_terminal_size()
BANNER = r"""
 __  __     ______     ______     __         ______     ______     ______    
/\ \/\ \   /\  ___\   /\  ___\   /\ \       /\  ___\   /\  ___\   /\  ___\   
\ \ \_\ \  \ \___  \  \ \  __\   \ \ \____  \ \  __\   \ \___  \  \ \___  \  
 \ \_____\  \/\_____\  \ \_____\  \ \_____\  \ \_____\  \/\_____\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/ 
                                                                             
 __    __     ______     ______     __  __     __     __   __     ______     
/\ "-./  \   /\  __ \   /\  ___\   /\ \_\ \   /\ \   /\ "-.\ \   /\  ___\    
\ \ \-./\ \  \ \  __ \  \ \ \____  \ \  __ \  \ \ \  \ \ \-.  \  \ \  __\    
 \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\  \ \_\\"\_\  \ \_____\  
  \/_/  \/_/   \/_/\/_/   \/_____/   \/_/\/_/   \/_/   \/_/ \/_/   \/_____/  

"""

def get_messages(file_name:str) -> Dict:
    """
    Reads and retrieves messages from a JSON file.

    Args:
        file_name (str): The name of the JSON file containing the messages.

    Returns:
        dict: A dictionary containing the messages.
    """
    with open(file_name, encoding='utf8') as messages_json:
        messages_dict = json.load(messages_json)
    messages_size = len(messages_dict["interactions"]) 
    return messages_dict, messages_size

def get_farewells(farewell_file:str) -> Dict:
    with open(farewell_file, encoding='utf8') as farewell_json:
        farewell_dict = json.load(farewell_json)
    return farewell_dict

def show_farewell(farewell:Dict) -> None:
    translation = '"' + farewell["translation"]["literal"] + '"'
    origin = tr.wrap(f'{farewell["origin"]}', width=80)
    language = "in " + farewell["language"]
    print(farewell["message"].center(TERM_WIDTH), end="\n"*2)
    sleep(1)
    print("Wich means (literally)".center(TERM_WIDTH), end="\n")
    print(translation.center(TERM_WIDTH), end="\n")
    print(language.center(TERM_WIDTH), end="\n"*2)
    sleep(1)
    for origin_line in origin:
        print(origin_line.center(TERM_WIDTH))
    print("\n"*3)
    sleep(1)
    return None

def generate_new_message() -> Dict:
    farewells = get_farewells(FAREWELL_FILE)
    new_message = farewells[ str(randrange(len(farewells))+1) ]
    return new_message

def save_message(message:str) -> Dict:
    messages_history, last_id = get_messages(DATA_SOURCE)
    new_id = last_id + 1
    messages_history["interactions"].append({"id" : new_id, "message" : message})
    with open(DATA_SOURCE, "w+", encoding='utf8') as messages_json:
        json.dump(messages_history, messages_json, indent=4, ensure_ascii=False)
    return messages_history

def fancy_counter(start: int) -> None:
    line_chars = LINE_LENGTH-2
    print("Turning off in\n".center(TERM_WIDTH))
    for counter in range(start,0,-1):
        # print(35*" ", end="")
        for frame in range(line_chars):
            animation = "*" + (line_chars-frame)*" " + "*"
            # fancy_filler = f'{animation: ^80}'
            # print("\r"*(len(fancy_filler)), fancy_filler, end="", flush="True")
            fancy_filler = animation.center(TERM_WIDTH)
            print("\r"*(len(fancy_filler)) + fancy_filler, end="", flush="True")
            sleep(0.01)
        counter_center = str(counter).center(TERM_WIDTH)
        print("\r"*(len(fancy_filler)), counter_center, end="", flush="True")
    sleep(.5)
    print()
    return None

def power_off(farewell_dict: Dict) -> None:
    save_message(farewell_dict)
    fancy_counter(REVERSE_COUNTER)
    show_farewell(farewell_dict)
    return None

def about(banner: str)->None:
    """
    Displays an about message with a custom banner.

    Args:
        banner (str): The custom banner to display.
    """
    for line in banner.splitlines():
        print(line.center(TERM_WIDTH))
    sleep(1)
    return None

def power_on() -> None:
    """
    Powers on the machine, generates a new message, saves it, and powers off.
    """
    about(BANNER)
    new_message = generate_new_message()
    power_off(new_message)
    return None

def main() -> None:
    power_on()
    return None

if __name__ == "__main__" :
    main()
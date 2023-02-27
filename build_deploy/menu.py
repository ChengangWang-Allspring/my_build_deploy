"""
1. Add a menu to a console application to manage activities.
2. Run a selected function.
3. Clear the output
4. Display the menu again or exit if done is selected
"""


import colorama
from colorama import Fore

import sys
from os import system
import time

from build_deploy import settings
from build_deploy.config_core import CicdConfig, Project
from build_deploy import config_core
from build_deploy import build_deploy


def display_main_menu(menu) -> None:
    """
    Display a menu where the key identifies the name of a function.
    :param menu: dictionary, key identifies a value which is a function name
    :return:
    """
    system('cls')
    print(Fore.GREEN + settings.LOGO)
    print('-' * 80)
    print(
        """ 
  Welcome to build and deploy. This is a utility to build .NET applications, 
  perform config transformation and deploy applications including ClickOnce 
  project cicd workflow is defined in cicd.yml.  Please select a project below.
    """
    )
    print('-' * 80)
    for k, project in menu.items():
        print(f'{k}: {project.name}')

    print(Fore.RESET)


def press_to_continue() -> None:
    input('press to continue')


def display_project_menu(project: Project) -> None:
    env: str = None
    while True:
        print(Fore.CYAN + 'you have selected: ' + f' {project.name} ' + Fore.RESET)
        print(
            Fore.CYAN + 'Enter an environment [dev|uat|prod|bcp] (enter q to exit): ' + Fore.RESET,
            end='',
        )
        env = input().lower()
        if env in ['q', 'exit', 'quit']:
            return
        if env not in ['dev', 'uat', 'prod', 'bcp']:
            print(
                Fore.RED + 'wrong environment. Must be one of these dev|uat|prod|bcp.' + Fore.RESET
            )
            continue
        else:
            print(Fore.CYAN + 'You have selected: ' + Fore.RESET + f'{env}')
            print(Fore.CYAN + 'Do you really want to continue ? [Yes|No]: ' + Fore.RESET, end='')
            prompt = input().lower()
            if prompt in ['yes', 'y']:
                print(Fore.YELLOW + 'Please wait ... ' + Fore.RESET)
                build_deploy.start_workflows(project, env)
                print(Fore.YELLOW + f'{env} build & deploy completed!' + Fore.RESET)
                press_to_continue()
                return
            else:
                return


def run():
    """main entrance of build and build"""

    # init colorama
    colorama.init()

    # parse and init CicdConfig
    config: CicdConfig = config_core.load_cicd_yaml()

    menu_items = dict(enumerate(config.projects, start=1))

    while True:
        display_main_menu(menu_items)
        print(Fore.CYAN + 'Select a number (enter q to exit): ' + Fore.RESET, end='')
        selection = None

        try:
            str_input = input()
            if str_input in ['q', 'exit', 'quit']:
                sys.exit()
            selection = int(str_input)  # Get function key
            if selection < 1 or selection > len(config.projects):
                raise ValueError()
        except ValueError:
            print(Fore.RED + 'invalid project number!' + Fore.RESET)
            press_to_continue()
            continue

        project_name = menu_items[selection]  # Gets the project name
        display_project_menu(project_name)

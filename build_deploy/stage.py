from colorama import Fore, Style

import subprocess
import sys
import shutil
import os
from pathlib import Path


from build_deploy import settings
from build_deploy import config_core
from build_deploy.config_core import Project, CicdConfig


def build(project: Project) -> None:
    """build C# project"""

    config = config_core._config
    print(Fore.GREEN)
    print(f' starting build {project.name} ... ')

    ms_build = config.ms_build_path if config.ms_build_path is not None else settings.MS_BUILD_PATH

    if not settings.solution_build_success:
        print(Fore.YELLOW + '=' * 80 + Fore.RESET)
        print(Fore.YELLOW + f' pre build solution: {config.solution_name} ... ' + Fore.RESET)
        print(Fore.YELLOW + '=' * 80 + Fore.RESET)
        exit_code: int = subprocess.call(
            [
                ms_build,
                config.solution_name,
                settings.ARG_1,
                settings.ARG_2,
                settings.ARG_3,
            ],
            shell=True,
        )
        if exit_code == 0:
            print(Fore.GREEN + '=' * 80 + Fore.RESET)
            print(Fore.GREEN + 'Buid Success!' + Fore.RESET)
            print(Fore.GREEN + '=' * 80 + Fore.RESET)
        else:
            print(Fore.RED + '=' * 80 + Fore.RESET)
            print(Fore.RED + 'Build Failure!' + Fore.RESET)
            print(Fore.RED + '=' * 80 + Fore.RESET)
            sys.exit()

    print(Fore.YELLOW + '=' * 80 + Fore.RESET)
    print(Fore.YELLOW + f' Build project: {project.project_path} ... ' + Fore.RESET)
    print(Fore.YELLOW + '=' * 80 + Fore.RESET)
    exit_code: int = subprocess.call(
        [
            ms_build,
            project.project_path,
            settings.ARG_1,
            settings.ARG_2,
            settings.ARG_3,
        ],
        shell=True,
    )
    if exit_code == 0:
        print(Fore.GREEN + '=' * 80 + Fore.RESET)
        print(Fore.GREEN + 'Buid Success!' + Fore.RESET)
        print(Fore.GREEN + '=' * 80 + Fore.RESET)
    else:
        print(Fore.RED + '=' * 80 + Fore.RESET)
        print(Fore.RED + 'Build Failure! Exiting app.' + Fore.RESET)
        print(Fore.RED + '=' * 80 + Fore.RESET)
        sys.exit()


def stage_binary(project: Project) -> None:
    """stage binary"""

    src_bin_dir = (
        Path.cwd().joinpath(project.project_path).parent.joinpath(settings.BIN_PATH).resolve()
    )
    work_bin_dir = Path.cwd().joinpath(settings.WORK_BIN_DIR).resolve()

    print(src_bin_dir)
    print(work_bin_dir)
    print(Fore.YELLOW + '=' * 80 + Fore.RESET)
    print(Fore.YELLOW + 'staging binary, please wait ... ' + Fore.RESET)
    print(Fore.YELLOW + '=' * 80 + Fore.RESET)
    shutil.copytree(src_bin_dir, work_bin_dir)


def build_deploy(project: Project, env: str) -> None:
    """build and deploy"""

    # clean up work dir
    cleanup_work_dir()

    # build(project)

    # stage binary
    stage_binary(project)

    # zip

    # upload artifact to artifactory

    # download artifact from artifactory

    # extract

    # config transformation

    # optional ClickOnce

    # deployment


def cleanup_work_dir():
    work_dir = Path.cwd().joinpath(settings.WORK_DIR)
    if work_dir.exists():
        print(f'removing {settings.WORK_DIR}')
        shutil.rmtree(work_dir)
    print(f'recreating {settings.WORK_BIN_DIR}')
    os.mkdir(work_dir)

from enum import Enum, auto

MS_BUILD_PATH: str = r'C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
CICD_YML: str = 'cicd.yml'  # yaml config file
WORK_DIR: str = '.cicd'  # temporary workspace folder
WORK_BIN_DIR: str = r'.cicd\bin'  # work bin dir
WORK_ZIP_DIR: str = r'.cicd\zip'  # work zip dir
WORK_EXTRACT_DIR: str = r'.cicd\extract'  # work extract dir
BIN_PATH = r'bin\x86\Release'  # msbuild output relative dir
ARG_1 = '/t:Rebuild'  # msbuild argument 1
ARG_2 = '/p:Configuration=Release'  # msbuild argument 2
ARG_3 = '/p:Platform=x86'  # msbuild argument 3


LOGO: str = r"""
 _           _ _     _       _            _             
| |__  _   _(_) | __| |   __| | ___ _ __ | | ___  _   _ 
| '_ \| | | | | |/ _` |  / _` |/ _ \ '_ \| |/ _ \| | | |
| |_) | |_| | | | (_| | | (_| |  __/ |_) | | (_) | |_| |
|_.__/ \__,_|_|_|\__,_|  \__,_|\___| .__/|_|\___/ \__, |
                                   |_|            |___/ 
"""


solution_build_success: bool = False

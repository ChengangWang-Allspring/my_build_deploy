from enum import Enum, auto

CICD_YML: str = 'cicd.yml'  # yaml config file
MS_BUILD_PATH: str = r'C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe'
MS_BUILD_CLICKONCE_PATH: str = r'%WINDIR%\Microsoft.NET\Framework\v4.0.30319\msbuild.exe'
ARTIFACT_S3_URL = 's3://s3-agtps01-use-dev/artifacts/'

""" workspace folders """
WORK_DIR: str = '.cicd'  # temporary workspace folder
WORK_BIN_DIR: str = 'bin'  # work bin dir
WORK_EXTRACT_DIR: str = 'extract'  # work extract dir
WORK_CLICKONCE_TEMP_DIR: str = 'clickonce_temp'  # clickonce temp dir


""" msbuild related arguments """
PROJECT_BIN_PATH = r'bin\x86\Release'  # msbuild output relative dir
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

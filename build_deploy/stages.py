from colorama import Fore

import subprocess
import sys
import shutil
import os
from pathlib import Path
import fnmatch
import glob
import re


from build_deploy import settings
from build_deploy import config_core
from build_deploy.config_core import Project, CicdConfig


def check_duplicate_artifact(project: Project) -> bool:
    """check if version-artifact exist"""
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(
        Fore.CYAN
        + f'Check if artifact of the same version already exist: {project.artifact_name}'
        + Fore.RESET
    )
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    if artifact_exist(project):
        print(
            Fore.RED
            + 'This version of artifact exists on FSX. To build, you need to either change the version in CICD.yml or remove the artifact manually from FSX '
            + Fore.RESET
        )
        print(f'artifact fsx path: {settings.ARTIFACT_FSX_PATH}')

        return True
    else:
        return False


def build(project: Project) -> None:
    """build C# project"""

    config: CicdConfig = config_core._config
    print(Fore.CYAN + f' starting build {project.name} ... ' + Fore.RESET)

    ms_build = config.ms_build_path if config.ms_build_path is not None else settings.MS_BUILD_PATH

    if not settings.solution_build_success:
        print(Fore.CYAN + '=' * 80 + Fore.RESET)
        print(Fore.CYAN + f' pre build solution: {config.solution_name} ... ' + Fore.RESET)
        print(Fore.CYAN + '=' * 80 + Fore.RESET)
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

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f' Build project: {project.project_path} ... ' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
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


def prepare_artifacts(project: Project) -> None:
    """stage binary from VS project bin to workspace bin"""

    src_bin_dir = (
        Path.cwd()
        .joinpath(project.project_path)
        .parent.joinpath(settings.PROJECT_BIN_PATH)
        .resolve()
    )
    work_bin_dir = Path.cwd().joinpath(settings.WORK_DIR).joinpath(settings.WORK_BIN_DIR).resolve()

    print(src_bin_dir)
    print(work_bin_dir)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + 'staging binary, please wait ... ' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    shutil.copytree(src_bin_dir, work_bin_dir, dirs_exist_ok=True)


def cleanup_work_dir():
    """clean up workspace and reset required folders"""

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f'Cleaning up work dir: {settings.WORK_DIR}' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    work_dir = Path.cwd().joinpath(settings.WORK_DIR)
    if work_dir.exists():
        print(f'removing {settings.WORK_DIR}')
        shutil.rmtree(work_dir)

    print(f'creating {work_dir} ... ')
    os.mkdir(work_dir)

    print(f'creating {work_dir.joinpath(settings.WORK_BIN_DIR)}')
    os.mkdir(work_dir.joinpath(settings.WORK_BIN_DIR))

    print(f'creating {work_dir.joinpath(settings.WORK_EXTRACT_DIR)}')
    os.mkdir(work_dir.joinpath(settings.WORK_EXTRACT_DIR))

    print(f'creating {work_dir.joinpath(settings.WORK_CLICKONCE_TEMP_DIR)}')
    os.mkdir(work_dir.joinpath(settings.WORK_CLICKONCE_TEMP_DIR))


def zip_artifacts(project: Project):
    """zip the artifacts in workspace bin dir"""

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(
        Fore.CYAN
        + f'Zip the artifacts from : {settings.WORK_DIR}/{settings.WORK_BIN_DIR}'
        + Fore.RESET
    )
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    print(f'project artifact_name: {project.artifact_name}')
    zip_base_name = Path.cwd().joinpath(settings.WORK_DIR).joinpath(project.artifact_name).resolve()
    root_dir = Path.cwd().joinpath(settings.WORK_DIR).resolve()

    shutil.make_archive(zip_base_name, 'zip', root_dir, settings.WORK_BIN_DIR)


def extract_artifacts(project: Project):
    """extract the artifacts to workspace extract dir"""

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(
        Fore.CYAN
        + f'Extract artifactor to: {settings.WORK_DIR}/{settings.WORK_EXTRACT_DIR}'
        + Fore.RESET
    )
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    zip_name = f'{project.artifact_name}.zip'
    zip_name = Path.cwd().joinpath(settings.WORK_DIR).joinpath(zip_name).resolve()
    extract_dir = (
        Path.cwd().joinpath(settings.WORK_DIR).joinpath(settings.WORK_EXTRACT_DIR).resolve()
    )
    print(zip_name)
    print(extract_dir)

    if extract_dir.exists():
        print(f'removing {extract_dir}')
        shutil.rmtree(extract_dir)

    print(f'creating {extract_dir} ... ')
    os.mkdir(extract_dir)

    shutil.unpack_archive(zip_name, extract_dir, 'zip')


def transform_config(env: str):
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f'Starting "Config Transform" for: {env} ...' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    bin_path = (
        Path.cwd()
        .joinpath(settings.WORK_DIR)
        .joinpath(settings.WORK_EXTRACT_DIR)
        .joinpath(settings.WORK_BIN_DIR)
    )
    config_path = bin_path.joinpath('Config')
    if not config_path.exists():
        print(Fore.YELLOW + '=' * 80 + Fore.RESET)
        print(
            Fore.YELLOW
            + f'WARNING: "Config" directory does not exist!! "Config Transform" skipped ...'
            + Fore.RESET
        )
        print(Fore.YELLOW + '=' * 80 + Fore.RESET)
        return

    exe_config_path = bin_path.joinpath('*.exe.config').resolve()
    exe_config_file = None
    for file in glob.glob(str(exe_config_path)):
        exe_config_file = file  # assuming there is only one exe_config_file
        break

    files = os.listdir(config_path)
    match = fnmatch.filter(files, f'*.{env}.config')
    for file in match:
        if file.lower() == f'app.{env}.config' and exe_config_file is not None:
            source_path = config_path.joinpath(file).resolve()
            target_path = exe_config_file
            print(f'copying from {source_path} to {target_path}')
            shutil.copyfile(source_path, target_path)
        else:
            source_path = config_path.joinpath(file).resolve()
            # use regular expression to do replacement ignore case
            compiled = re.compile(re.escape(f'{env}.'), re.IGNORECASE)
            target_path = bin_path.joinpath(compiled.sub('', file))
            print(f'copying from {source_path} to {target_path}')
            shutil.copyfile(source_path, target_path)

    print('Config transformation success! ')


def clickonce_manifest(project: Project, env: str):
    """run msbuild clickonce script to setup clickonce binaries including manifest and signing"""

    if project.clickonce_project_path is None:
        return

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f'Starting ClickOnce build for: {env} ...' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    proj_path = Path(project.clickonce_project_path)
    if not proj_path.exists() or not proj_path.is_file():
        raise Exception('Not a valid ClickOnce project file!')
        return

    deploy_path = project.deploy_path.__getattribute__(env)
    workspace_path = Path.cwd().joinpath(settings.WORK_DIR)
    source_bin_path = workspace_path.joinpath(settings.WORK_EXTRACT_DIR).joinpath('bin')
    app_path = proj_path.parent.parent
    clickonce_temp_path = workspace_path.joinpath(settings.WORK_CLICKONCE_TEMP_DIR)

    print(f'project.version = {project.version}')
    print(f'deploy_path = {deploy_path}')
    print(f'source_bin_path = {source_bin_path.resolve()}')
    print(f'app_path = {app_path.resolve()}')
    print(f'env = {env}')
    print(f'clickonce_temp_path = {clickonce_temp_path.resolve()}')

    args_1 = f'/p:PublishVersion={project.version}'
    args_2 = f'/p:FinalDeployPath={deploy_path}'
    args_3 = f'/p:SourceDir={source_bin_path.resolve()}'
    args_4 = f'/p:AppPath={app_path.resolve()}'
    args_5 = f'/p:Environment={env}'
    args_6 = f'/p:PublishTempParentDir={clickonce_temp_path.resolve()}'

    exit_code: int = subprocess.call(
        [
            settings.MS_BUILD_CLICKONCE_PATH,
            project.clickonce_project_path,
            '/v:n',
            args_1,
            args_2,
            args_3,
            args_4,
            args_5,
            args_6,
        ],
        shell=True,
    )
    if exit_code == 0:
        print(Fore.CYAN + f'Renaming extensions to *.deploy' + Fore.RESET)
        for path, dirs, files in os.walk(clickonce_temp_path):
            for file in files:
                if not file.endswith('.manifest') and not file.endswith('.application'):
                    os.rename(os.path.join(path, file), os.path.join(path, file + '.deploy'))


def deploy_files(project: Project, env: str):
    """deploy files to target location"""

    deploy_path = project.deploy_path.__getattribute__(env)

    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f'Deploying files ... ' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(f'env: {env}')
    print(f'deploy_path: {deploy_path}')
    print(f'clean_target: {project.clean_target}')

    if project.clean_target:
        print(Fore.CYAN + f'cleaning target files and directories from deploy_path ' + Fore.RESET)
        for path, dirs, files in os.walk(deploy_path, topdown=False):
            for name in files:
                os.remove(os.path.join(path, name))
            for name in dirs:
                os.rmdir(os.path.join(path, name))

    if project.clickonce_project_path is not None:
        source_bin = (
            Path.cwd()
            .joinpath(settings.WORK_DIR)
            .joinpath(settings.WORK_CLICKONCE_TEMP_DIR)
            .resolve()
        )
    else:
        source_bin = (
            Path.cwd()
            .joinpath(settings.WORK_DIR)
            .joinpath(settings.WORK_EXTRACT_DIR)
            .joinpath('bin')
            .resolve()
        )
    print(Fore.CYAN + f'Copying from "{source_bin}" to "{deploy_path}" ... ' + Fore.RESET)
    shutil.copytree(source_bin, deploy_path, dirs_exist_ok=True)


def artifact_exist(project: Project) -> bool:
    zip_path = os.path.join(settings.ARTIFACT_FSX_PATH, project.artifact_name + '.zip')
    return os.path.exists(zip_path)


def upload_artifact(project: Project):
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(Fore.CYAN + f'Preparing to upload artifact: {project.artifact_name}.zip ...' + Fore.RESET)
    print(Fore.CYAN + f'Artifact FSX Path: {settings.ARTIFACT_FSX_PATH}' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    if not artifact_exist(project):
        # upload if artifact-name not exist

        source_file_path = (
            Path.cwd().joinpath(settings.WORK_DIR).joinpath(project.artifact_name + '.zip')
        )
        print(f'source_file_path: {source_file_path}')
        dest_file_path = os.path.join(settings.ARTIFACT_FSX_PATH, project.artifact_name + '.zip')
        shutil.copy2(source_file_path, dest_file_path)

    else:
        raise FileExistsError(
            f'Artifact name "{project.artifact_name}.zip" already exists on FSX share: {settings.ARTIFACT_FSX_PATH}'
        )


def download_artifact(project: Project):
    print(Fore.CYAN + '=' * 80 + Fore.RESET)
    print(
        Fore.CYAN + f'Preparing to download artifact: {project.artifact_name}.zip ...' + Fore.RESET
    )
    print(Fore.CYAN + f'FSX Share: {settings.ARTIFACT_FSX_PATH}' + Fore.RESET)
    print(Fore.CYAN + '=' * 80 + Fore.RESET)

    if artifact_exist(project):
        # upload if artifact-name not exist

        target_file_path = (
            Path.cwd().joinpath(settings.WORK_DIR).joinpath(project.artifact_name + '.zip')
        )
        print(f'target_file_path: {target_file_path}')
        source_file_path = os.path.join(settings.ARTIFACT_FSX_PATH, project.artifact_name + '.zip')
        shutil.copy2(source_file_path, target_file_path)

    else:
        raise FileExistsError(
            f'Artifact name "{project.artifact_name}.zip" NOT exist on FSX Share: {settings.ARTIFACT_FSX_PATH}'
        )

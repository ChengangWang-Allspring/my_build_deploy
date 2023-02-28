from colorama import Fore, Style

import traceback
import sys

from build_deploy.config_core import Project
from build_deploy import stages


def start_workflows(project: Project, env: str) -> None:
    """build and deploy"""

    try:
        """clean up work dir"""
        stages.cleanup_work_dir()

        """ build the project """
        stages.build(project)

        """ stage binary """
        stages.prepare_artifacts(project)

        """ zip """
        stages.zip_artifacts(project)

        """ upload artifact to artifactory """
        # Furture use artifactory to replace S3 bucket
        stages.upload_artifact(project)

        # Future TODO in Jenkins or Ansible
        # download artifact from artifactory

        """ extract zip """
        stages.extract_artifacts(project)

        """ config transformation """
        stages.transform_config(env)

        """ ClickOnce manifest steps if needed """
        stages.clickonce_manifest(project, env)

        """ deployment file copy """
        stages.deploy_files(project, env)

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + '=' * 80)
        print('Error caught in build_deploy !! ')
        print(e)
        print('**' + type(e).__name__ + '**')
        print(traceback.format_exc())
        print('Exit 500' + Fore.RESET + Style.RESET_ALL)
        sys.exit(500)


def main():
    pass


if __name__ == '__main__':
    main()

from build_deploy.config_core import Project
from build_deploy import stages


def start_workflows(project: Project, env: str) -> None:
    """build and deploy"""

    """  clean up work dir """
    stages.cleanup_work_dir()

    """ build the project """
    stages.build(project)

    """ stage binary """
    stages.prepare_artifacts(project)

    """ zip """
    stages.zip_artifacts(project)

    """ upload artifact to artifactory """
    # TODO

    """ download artifact from artifactory """
    # TODO

    """ extract zip """
    stages.extract_artifacts(project)

    """ config transformation """
    stages.transform_config(env)

    """ ClickOnce manifest steps if needed """
    stages.clickonce_manifest(project, env)

    """ deployment file copy """
    stages.deploy_files(project, env)

def main():
    pass


if __name__ == '__main__':
    main()

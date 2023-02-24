import yaml
from pydantic import BaseModel, validator, root_validator
from typing import List, Optional


from build_deploy import settings


class DeployPath(BaseModel):
    dev: str
    uat: str
    prod: str
    bcp: str


class Project(BaseModel):
    name: str
    version: str
    project_path: str
    deploy_path: DeployPath
    clickonce_project_path: Optional[str]


class CicdConfig(BaseModel):
    ms_build_path: Optional[str]
    solution_name: str
    projects: List[Project]


_config: CicdConfig = None


def load_cicd_yaml() -> CicdConfig:
    my_dict: dict = None
    with open(settings.CICD_YML, "r") as f:
        my_dict: dict = yaml.safe_load(f)
    # print(my_dict)
    global _config
    _config = CicdConfig(**my_dict)
    return _config

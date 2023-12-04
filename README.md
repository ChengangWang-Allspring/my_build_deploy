# Python build_deploy
Python based build and deploy for Visual Studio .NET projects

## Description
A short-term CICD solution for Portfolio Management .NET apps.

## Getting Started
Check the ClickOnce demo in this GitHub location. There is an example cicd yml file you can model after.
https://github.com/Allspring-Cloud/agtps-core/tree/ClickOnce_Demo


### cicd.yml syntax
- solution_name: required entry point solution file name.
- the cicd.yml file is pretty self explanatory.
- the cicy.yml file needs to be located in the same folder as Visual Studio solution folder
- name: application name that will be installed in add/remove or start menu
- clean_target: clean output directory before xcopying
- deploy_path: deployment UNC share for different environment
- clickonce_project_path: required `cicd_clickonce.proj` file for ClickOnce manifest signing to work
- Check with Chenggang if you have additional questions for build_deploy
# Introduction

# Project Structure
```
.
└── {{cookiecutter.directory_name}}/
    ├── config/
    │   └── config.py
    ├── data/
    ├── logs/
    ├── models/
    ├── notebooks/
    │   └── 00_prototyping.ipynb
    ├── {{cookiecutter.project_slug}}/
    │   ├── data.py
    │   ├── main.py
    │   ├── predict.py
    │   ├── train.py
    │   └── utils.py
    ├── Makefile
    ├── pyproject.toml
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

# Getting Started
In order to use the training functions and generate a new language model you first need to setup the virtual environment to ensure all dependencies are met.

## Setting up virtual environment
1. While in the root directory of the project, create a `venv` folder with **python {{cookiecutter.python_version}}**
```bash
python3 -m venv venv
```
after this you should be able to see a folder called `venv` within the project.


2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install {{cookiecutter.project_slug}} package to use it
```bash
make env
```
If you'd like to contribute to the project run the following command instead for other additional packages that ensure styling and repo consistency
```bash
make devenv
```

# Using the package


# Contributing
If you are going to make changes to this project make sure to create an environment with the
```bash
make devenv
```
command as stated in the **Getting Started** section in order to make every commit of code consistent with the rest of the codebase and styling.


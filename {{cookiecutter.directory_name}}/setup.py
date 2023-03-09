from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

style_packages = ["black", "flake8", "isort", "pylint", "jupyter-black"]

# Define package
setup(
    name="{{cookiecutter.project_slug}}",
    version="0.0.1",
    description="{{cookiecutter.project_description}}",
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.email}}",
    python_requires="=={{cookiecutter.python_version}}",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={"dev": style_packages + ["pre-commit"]},
)

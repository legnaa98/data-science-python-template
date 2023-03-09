FROM python:{{cookiecutter.python_version}}-slim
WORKDIR /src
COPY setup.py setup.py
COPY config config
COPY requirements.txt requirements.txt
COPY Makefile Makefile
RUN apt-get update && apt-get install make \
    && make env
COPY {{cookiecutter.project_slug}} {{cookiecutter.project_slug}}
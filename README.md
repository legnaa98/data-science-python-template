# data-science-python-template
A simple Data Science cookiecutter project template, with commonly used functions within the `utils.py` module for tasks such:
* Read/write operations on various data formats from local directories or S3 buckets
* List all URIs within an S3 bucket
* And, saving pandas dataframes in S3 as parquet or csv

## Usage
There is no need to clone this repo locally. Just make sure to install cookiecutter in your machine
```bash
pip install cookiecutter
```
And then you can create a new project structure
```bash
cookiecutter https://github.com/legnaa98/data-science-python-template
```
After the execution of the previous command, you will be able to see a directory with the name that you assigned to your project.

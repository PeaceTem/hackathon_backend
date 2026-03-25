#!/bin/bash

# move into the hackathon subfolder
# cd hackathon

# create virtual environment in the project root
python3 -m venv venv

# activate the virtual environment
. venv/bin/activate

# upgrade pip
pip install --upgrade pip

# install dependencies from requirements.txt in the project root
pip install -r hackathon/requirements.txt

# collect static files
python hackathon/manage.py collectstatic --noinput
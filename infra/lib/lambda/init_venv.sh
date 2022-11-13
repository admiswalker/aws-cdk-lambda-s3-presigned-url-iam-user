#!/bin/bash

PRJ_NAME=pyenv
python3 -m venv ${PRJ_NAME}
source ${PRJ_NAME}/bin/activate
pip install -r requirements.txt


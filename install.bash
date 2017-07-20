#!/bin/bash

# create virtualenv
python3 -m venv venv

# activate virtualenv
source venv/bin/activate

# install requirements.txt
pip install -r requirements.txt

# run server
python3 test1.py -h 0.0.0.0

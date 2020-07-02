#!/bin/bash

python -m venv env
chmod +x env/bin/activate
source env/bin/activate

pip install -r requirements.txt
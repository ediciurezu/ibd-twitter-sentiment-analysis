#!/bin/bash
cd backend

python3 -m venv virtualenv
source /virtualenv/bin/activate
pip install boto3
pip install flask_cors

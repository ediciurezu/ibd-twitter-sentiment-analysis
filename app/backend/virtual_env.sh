#!/bin/bash

python3 -m venv virtualenv
source virtualenv/bin/activate
pip install boto3
pip install flask_cors
pip install flask_socketio
pip install praw
pip install langdetect
pip install pandas
pip install regex
pip install textblob

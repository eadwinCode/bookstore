#!/usr/bin/env bash

# Script to run the Django server in a development environment

python3 bookstore/manage.py migrate
python3 bookstore/manage.py runserver 0.0.0.0:8001
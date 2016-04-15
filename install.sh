#!/usr/bin/env bash

sudo apt-get install -y python-pip
sudo pip install virtualenv

virtualenv venv
source ./env.sh

pip install -r requirements.txt

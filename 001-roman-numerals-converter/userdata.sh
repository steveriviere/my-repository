#!/bin/bash
yum update -y
yum install python3 -y
yum install pip -y
pip install flask
cd /home/ec2-user/
FOLDER="https://raw.githubusercontent.com/steveriviere/my-repository/refs/heads/main/001-roman-numerals-converter/"
wget ${FOLDER}/app.py
mkdir templates
cd templates
wget ${FOLDER}/templates/index.html
wget ${FOLDER}/templates/result.html
cd..
python3 app.py




#### you can use code below to download whole subfolder in a repository

git clone --no-checkout https://github.com/steveriviere/my-repository/
cd my-repository
git sparse-checkout init --cone
git sparse-checkout set 001-roman-numerals-converter
git checkout
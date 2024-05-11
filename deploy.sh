#!/bin/bash

cd src
git clean energy_meter/ -fdx
mpremote fs cp -r energy_meter : + \
    fs cp config.py : + \
    fs cp main.py : + \
    fs cp boot.py : + \
    fs cp secrets.py :
cd -


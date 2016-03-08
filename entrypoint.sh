#!/bin/bash

if [[ -z "$access_address" ]];
then
    echo "Please provide access_address"
    exit 1
fi

cd /opt/tutu
python app.py --access_address="$access_address"

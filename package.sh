#!/bin/bash

rm tutu.tar.gz;
bower install
tar --exclude='*.json' --exclude='README.md' --exclude='node_modules' --exclude='.git' --exclude='**.pyc' --exclude='**.scss' --exclude='**.less' --exclude='tests' --exclude='**.pub' --exclude='setup.cfg' --exclude='run-test.sh'  --exclude='package.sh' -zcvf tutu.tar.gz .

#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`pwd`
nosetests tests

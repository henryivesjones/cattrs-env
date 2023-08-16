#!/bin/bash
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..

python3 -m venv .test-venv
source .test-venv/bin/activate

pip3 install -r test-requirements.txt
pip3 install .

python3 -m coverage run -m unittest

python3 -m coverage report -m

#!/bin/bash
# Update pip để xóa warning
python -m pip install --upgrade pip
# Install requirements
pip install -r requirements.txt
# Install package
pip install -e .

#!/bin/bash
echo "Activating virtual environment" & 
source env/bin/activate &
echo "Obtaining requirements list." &&
pip freeze > requirements.txt &&
echo "Generating pyproject.toml." &&
python3 -m scripts.build_pyproject_toml &&
echo "Clearing dist/ folder" &&
rm -rf dist/*
echo "Building project." &&
python3 -m build &&
echo "Done."
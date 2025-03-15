#!/bin/bash

# runs the unit tests
cd "$(dirname "$0")/.."  # commands to move to  root directory
PYTHONPATH=. python3 -m unittest discover test

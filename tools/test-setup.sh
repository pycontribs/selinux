#!/bin/bash

# NOTE(pabelanger): Default to pip3, when possible this is because python2
# support is EOL.
PYTHON=$(command -v python3 python2 | head -n1)

# NOTE(pabelanger): Tox on centos-7 is old, so upgrade it across all distros
# to the latest version
sudo $PYTHON -m pip install -U tox "zipp<0.6.0;python_version=='2.7'"

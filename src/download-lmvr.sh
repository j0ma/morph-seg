#!/bin/bash

set -eo pipefail
ROOT=$(dirname "$0")

# by default, the LMVR will be downloaded to ~/lmvr/lmvr-repo,
# and the virtual environment installed in ~/lmvr/lmvr-env.
# these can obviously be overridden by setting the environment vairables.
if [ -z "$LMVR_PATH" ] || [ -z "$LMVR_ENV_PATH" ]; then
    echo "Using default values..."
    source "$ROOT/lmvr-environment-variables.sh"
fi

# remove existing installations
rm -Rf "$LMVR_PATH" "$LMVR_ENV_PATH"

git clone https://github.com/d-ataman/lmvr "$LMVR_PATH"

# you can also customize the python 2.7 executable you give
# virtualenv. by default we use $(which python2), and assume
# the user normally runs python 3
if [ -z "$PYTHON2_EXECUTABLE" ]; then
    PYTHON2_EXECUTABLE=$(which python2)
fi

virtualenv "$LMVR_ENV_PATH" --python="$PYTHON2_EXECUTABLE"

# install
cd "$LMVR_PATH"
source "$LMVR_ENV_PATH/bin/activate"
python setup.py install

#!/bin/bash

set -euo pipefail

cd $(dirname $0)/..

echo "Compiling main requirements"
pip-compile --quiet requirements.in "$@"

echo "Compiling development requirements"
pip-compile --quiet requirements-dev.in "$@"

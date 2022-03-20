#!/bin/bash

# Let's source on root as PATH is already setup
source /root/.bashrc

which pre-commit >/dev/null && pre-commit install --install-hooks
#fuser -k 8003/tcp
yarn install --non-interactive
webpack --devtool eval-cheap-module-source-map --bail
echo "Packaging done!"



#!/bin/sh

set -e

./bin/coverage run \
    --source src/yafowil/widget/select2 \
    --omit src/yafowil/widget/select2/example.py \
    -m yafowil.widget.select2.tests
./bin/coverage report
./bin/coverage html

#!/usr/bin/env sh

apk --update add make
make deps
make deps-dev

python run.py
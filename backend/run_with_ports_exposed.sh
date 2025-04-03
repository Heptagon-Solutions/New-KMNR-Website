#!/bin/bash

# Runs backend with ports exposed to LAN
# Note that this is for development only; the flask command is NOT meant for production, and using `host=0.0.0.0` is not exactly secure.
pipenv run python3 -m flask run --host=0.0.0.0

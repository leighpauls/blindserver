#!/bin/sh

export PATH="$HOME/miniconda3/bin:$PATH"

cd "$HOME/src/blindserver"
waitress-serve app:app

#!/bin/sh

export PATH="$HOME/miniconda3/bin:$PATH"

echo $PATH
which python
exec python ~/src/blindserver/pi_client.py

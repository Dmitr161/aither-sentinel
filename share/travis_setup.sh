#!/bin/bash
set -evx

mkdir ~/.aithercore

# safety check
if [ ! -f ~/.aithercore/aither.conf ]; then
  cp share/aither.conf.example ~/.aithercore/aither.conf
fi

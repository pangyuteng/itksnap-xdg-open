#!/bin/bash
export CITKSNAP_URI=$@
# use a sh file to do simple prep work as oppose to a py script.

python3 gui.py ${CITKSNAP_URI} /tmp/ok

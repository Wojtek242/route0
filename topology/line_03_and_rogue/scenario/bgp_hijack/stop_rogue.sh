#!/bin/bash

SCRIPT=$(readlink -f $0)
DIRNAME=$(dirname $SCRIPT)

sudo python $DIRNAME/../../../../attach.py --node R4 --cmd "pgrep -u frr -f R4-zebra | xargs -r kill -9"
sudo python $DIRNAME/../../../../attach.py --node R4 --cmd "pgrep -u frr -f R4-bgpd | xargs -r kill -9"

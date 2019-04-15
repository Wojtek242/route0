#!/bin/bash

node=${1:-h1_1}
bold=`tput bold`
normal=`tput sgr0`

SCRIPT=$(readlink -f $0)
DIRNAME=$(dirname $SCRIPT)

while true; do
    out=`sudo python $DIRNAME/../../../../attach.py --node $node --cmd "curl -s 13.0.1.1"`
    date=`date`
    echo $date -- $bold$out$normal
    sleep 1
done

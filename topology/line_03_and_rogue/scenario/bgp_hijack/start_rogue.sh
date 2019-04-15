#!/bin/bash

SCRIPT=$(readlink -f $0)
DIRNAME=$(dirname $SCRIPT)

echo "Killing any existing rogue AS"
$DIRNAME/stop_rogue.sh

echo "Starting rogue AS"
sudo python $DIRNAME/../../../../attach.py --node R4 \
     --cmd "/usr/lib/frr/zebra -f $DIRNAME/../../zebra/R4.conf.rogue -d -i /tmp/R4-zebra.pid > /tmp/R4-zebra.out"
sudo python $DIRNAME/../../../../attach.py --node R4 \
     --cmd "/usr/lib/frr/bgpd -f $DIRNAME/bgpd/R4.conf.rogue -d -i /tmp/R4-bgpd.pid > /tmp/R4-bgpd.out"

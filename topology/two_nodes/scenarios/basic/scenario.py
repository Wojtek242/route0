#!/usr/bin/env python

import os
import sys

from mininet.net import Mininet
from mininet.cli import CLI

topo_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../..')
sys.path.append(topo_dir)
from topo import NetTopo

root_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../../../..')
sys.path.append(root_dir)
from router import Router


def scenario():
    """Start the network scenario.
    """

    os.system("rm -f /tmp/R*.log /tmp/R*.pid /tmp/R*.out")
    os.system("rm -f /tmp/h*.log /tmp/h*.pid /tmp/h*.out")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra staticd > /dev/null 2>&1")

    net = Mininet(topo=NetTopo(), switch=Router)
    net.start()

    for node in net.switches:
        # Start Zebra (routing table daemon)
        node.cmd("/usr/lib/frr/zebra"
                 " -f two-nodes/zebra/%s.conf"
                 " -d"
                 " -i /tmp/%s-zebra.pid"
                 " > /tmp/%s-zebra.out 2>&1"
                 % (node.name, node.name, node.name))
        node.waitOutput()

        if node.name.startswith('h'):
            # Start static route daemon
            node.cmd("/usr/lib/frr/staticd"
                     " -f two-nodes/staticd/%s.conf"
                     " -d"
                     " -i /tmp/%s-staticd.pid"
                     " > /tmp/%s-staticd.out 2>&1"
                     % (node.name, node.name, node.name))
            node.waitOutput()

        if node.name.startswith('R'):
            # Enable IP forwarding
            node.cmd("sysctl -w net.ipv4.ip_forward=1")
            node.waitOutput()

            # Delete spare loopback address for convenience
            node.cmd("ip addr del 127.0.0.1/8 dev lo")
            node.waitOutput()

    CLI(net)
    net.stop()
    os.system("killall -9 zebra staticd")


if __name__ == "__main__":
    scenario()

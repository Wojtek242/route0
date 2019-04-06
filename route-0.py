#!/usr/bin/env python

import os

from mininet.net import Mininet
from mininet.cli import CLI

from router import Router
from topology.two_nodes.topo import NetTopo as TwoNodes


def run(topo):
    """Start a network scenario.
    """

    os.system("rm -f /tmp/R*.log /tmp/R*.pid /tmp/R*.out")
    os.system("rm -f /tmp/h*.log /tmp/h*.pid /tmp/h*.out")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra staticd > /dev/null 2>&1")

    net = Mininet(topo=topo(), switch=Router)
    net.start()

    for node in net.switches:
        # Start Zebra (routing table daemon)
        node.cmd("/usr/lib/frr/zebra"
                 " -f %s/zebra/%s.conf"
                 " -d"
                 " -i /tmp/%s-zebra.pid"
                 " > /tmp/%s-zebra.out 2>&1"
                 % (topo.topo_dir, node.name, node.name, node.name))
        node.waitOutput()

        if node.name.startswith('h'):
            # Start static route daemon
            node.cmd("/usr/lib/frr/staticd"
                     " -f %s/staticd/%s.conf"
                     " -d"
                     " -i /tmp/%s-staticd.pid"
                     " > /tmp/%s-staticd.out 2>&1"
                     % (topo.topo_dir, node.name, node.name, node.name))
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
    run(TwoNodes)

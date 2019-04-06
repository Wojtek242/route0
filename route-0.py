#!/usr/bin/env python

import os

from mininet.net import Mininet
from mininet.cli import CLI

from router import Router
from topology.two_nodes.topo import NetTopo as TwoNodes
from scenario import Basic


def run(topo, scenario):
    """Start a network scenario.
    """

    os.system("rm -f /tmp/R*.log /tmp/R*.pid /tmp/R*.out")
    os.system("rm -f /tmp/h*.log /tmp/h*.pid /tmp/h*.out")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra staticd > /dev/null 2>&1")

    net = Mininet(topo=topo, switch=Router)
    net.start()
    scenario.setup(net)

    # WARNING: FRR can get confused unless all daemons on each node are started
    #          together.
    for node in net.switches:
        if node in scenario.routers:
            # Enable IP forwarding
            node.cmd("sysctl -w net.ipv4.ip_forward=1")
            node.waitOutput()

        if node in scenario.zebra:
            # Start Zebra (routing table daemon)
            node.cmd("/usr/lib/frr/zebra"
                     " -f %s/zebra/%s.conf"
                     " -d"
                     " -i /tmp/%s-zebra.pid"
                     " > /tmp/%s-zebra.out 2>&1"
                     % (topo.topo_dir, node.name, node.name, node.name))
            node.waitOutput()

            # Delete spare loopback address for convenience
            node.cmd("ip addr del 127.0.0.1/8 dev lo")
            node.waitOutput()

        if node in scenario.staticd:
            # Start static route daemon
            node.cmd("/usr/lib/frr/staticd"
                     " -f %s/staticd/%s.conf"
                     " -d"
                     " -i /tmp/%s-staticd.pid"
                     " > /tmp/%s-staticd.out 2>&1"
                     % (topo.topo_dir, node.name, node.name, node.name))
            node.waitOutput()

    CLI(net)
    net.stop()
    os.system("killall -9 zebra staticd")


if __name__ == "__main__":
    run(TwoNodes(), Basic())

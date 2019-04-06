#!/usr/bin/env python

import os
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..'))
from router import Router


class NetTopo(Topo):
    """The network topology.
    """

    def __init__(self):
        # Add default members to class.
        super(NetTopo, self).__init__()

        # The topology has one router per AS
        r_1 = self.addSwitch('R1')
        r_2 = self.addSwitch('R2')

        # Setup the links as follows:
        #
        # R1 --- R2
        #
        self.addLink(r_1, r_2)


def scenario():
    """Start the network scenario.
    """

    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra > /dev/null 2>&1")

    net = Mininet(topo=NetTopo(), switch=Router)
    net.start()
    for router in net.switches:
        # Enable IP forwarding
        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.waitOutput()

        # Start Zebra (routing table daemon)
        router.cmd("/usr/lib/frr/zebra"
                   " -f conf/zebra-%s.conf"
                   " -d"
                   " -i /tmp/zebra-%s.pid"
                   " > logs/%s-zebra-stdout 2>&1"
                   % (router.name, router.name, router.name))
        router.waitOutput()

        # Delete spare loopback address for convenience
        router.cmd("ip addr del 127.0.0.1/8 dev lo")
        router.waitOutput()

    CLI(net)
    net.stop()
    os.system("killall -9 zebra")


if __name__ == "__main__":
    scenario()

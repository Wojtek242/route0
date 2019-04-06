#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Switch, Node

import os

class Router(Switch):
    """Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.
    """
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    @staticmethod
    def setup():
        return

    def defaultIntf( self ):
        if hasattr(self, "controlIntf") and self.controlIntf:
            return self.controlIntf
        else:
            return Node.defaultIntf(self)

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()


class NetTopo(Topo):
    """The network topology.
    """
    def __init__(self):
        # Add default members to class.
        super(NetTopo, self ).__init__()

        # The topology has one router per AS
	routers = [
            self.addSwitch('R1'),
            self.addSwitch('R2'),
        ]
        hosts = []

        # Setup the links as follows:
        #
        # R1 --- R2
        #
        self.addLink('R1', 'R2')

        return


def main():
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
        router.cmd("/usr/lib/frr/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        router.waitOutput()

        # Delete spare loopback address for convenience
        router.cmd("ip addr del 127.0.0.1/8 dev lo")
        router.waitOutput()

    CLI(net)
    net.stop()
    os.system("killall -9 zebra")


if __name__ == "__main__":
    main()

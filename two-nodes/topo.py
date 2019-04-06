#!/usr/bin/env python

from mininet.topo import Topo


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

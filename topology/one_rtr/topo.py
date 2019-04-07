import os

from mininet.topo import Topo


class NetTopo(Topo):
    """The network topology.
    """

    def __init__(self):
        # Add default members to class.
        super(NetTopo, self).__init__()

        # Add routers
        r_1 = self.addSwitch('R1')

        # Add hosts
        h_1_1 = self.addSwitch('h1_1')
        h_2_1 = self.addSwitch('h2_1')

        # Setup links as shown in README.md
        self.addLink(r_1, h_1_1)
        self.addLink(r_1, h_2_1)

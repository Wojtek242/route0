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
        r_2 = self.addSwitch('R2')
        r_3 = self.addSwitch('R3')
        r_4 = self.addSwitch('R4')

        # Add hosts
        h_1_1 = self.addSwitch('h1_1')
        h_1_2 = self.addSwitch('h1_2')
        h_1_3 = self.addSwitch('h1_3')

        h_2_1 = self.addSwitch('h2_1')
        h_2_2 = self.addSwitch('h2_2')
        h_2_3 = self.addSwitch('h2_3')

        h_3_1 = self.addSwitch('h3_1')
        h_3_2 = self.addSwitch('h3_2')
        h_3_3 = self.addSwitch('h3_3')

        h_4_1 = self.addSwitch('h4_1')
        h_4_2 = self.addSwitch('h4_2')
        h_4_3 = self.addSwitch('h4_3')

        # Setup links as shown in README.md
        self.addLink(r_1, h_1_1)
        self.addLink(r_1, h_1_2)
        self.addLink(r_1, h_1_3)

        self.addLink(r_2, h_2_1)
        self.addLink(r_2, h_2_2)
        self.addLink(r_2, h_2_3)

        self.addLink(r_3, h_3_1)
        self.addLink(r_3, h_3_2)
        self.addLink(r_3, h_3_3)

        self.addLink(r_4, h_4_1)
        self.addLink(r_4, h_4_2)
        self.addLink(r_4, h_4_3)

        self.addLink(r_1, r_2)
        self.addLink(r_2, r_3)
        self.addLink(r_4, r_1)

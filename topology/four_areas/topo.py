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
        r_5 = self.addSwitch('R5')
        r_6 = self.addSwitch('R6')
        r_7 = self.addSwitch('R7')
        r_8 = self.addSwitch('R8')
        r_9 = self.addSwitch('R9')

        # Add hosts
        h_3_1 = self.addSwitch('h3_1')
        h_9_1 = self.addSwitch('h9_1')

        # Setup links as shown in README.md
        self.addLink(r_9, h_9_1)
        self.addLink(r_9, r_6)
        self.addLink(r_6, r_8)
        self.addLink(r_6, r_5)
        self.addLink(r_5, r_7)
        self.addLink(r_8, r_2)
        self.addLink(r_8, r_7)
        self.addLink(r_4, r_3)
        self.addLink(r_3, h_3_1)
        self.addLink(r_3, r_2)
        self.addLink(r_2, r_1)

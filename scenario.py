class Scenario(object):
    """Class that describes a network scenario.  A scenario defines which nodes
    are routers and which are hosts as well as which nodes need to start which
    daemons.

    """

    def __init__(self):
        self._routers = None
        self._hosts = None
        self._zebra = None
        self._staticd = None

    @property
    def routers(self):
        """Set of nodes that are routers.

        """
        return self._routers

    @property
    def hosts(self):
        """Set of nodes that are hosts.

        """
        return self._hosts

    @property
    def zebra(self):
        """Set of nodes that should run zebra.

        """
        return self._zebra

    @property
    def staticd(self):
        """Set of nodes that should run staticd.

        """
        return self._staticd

    def _routers_and_hosts(self, net):
        """Separate nodes into routers and hosts based on their names.

        """
        self._routers = set()
        self._hosts = set()

        for node in net.switches:
            if node.name.startswith('R'):
                self._routers.add(node)
            else:
                self._hosts.add(node)

    def setup(self, net):
        """Setup the scenario.

        """
        self._routers_and_hosts(net)
        self._zebra = set()
        self._staticd = set()


class Plain(Scenario):
    """In a Plain scenario no daemons are run.

    """


class Basic(Scenario):
    """In a Basic scenario, all nodes run zebra, and all hosts run staticd to
    setup a default route.

    """

    def __init__(self):
        Scenario.__init__(self)

    def setup(self, net):
        self._routers_and_hosts(net)
        self._zebra = self._routers.union(self._hosts)
        self._staticd = self._hosts

import os


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
        self._isisd = None

        self._zebra_conf = None
        self._staticd_conf = None
        self._isisd_conf = None

        self._reset()

    def _reset(self):
        self._routers = set()
        self._hosts = set()
        self._zebra = set()
        self._staticd = set()
        self._isisd = set()

        self._zebra_conf = None
        self._staticd_conf = None
        self._isisd_conf = None

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

    @property
    def isisd(self):
        """Set of nodes that should run isisd.

        """
        return self._isisd

    @property
    def zebra_conf(self):
        """Directory with zebra config files.

        """
        return self._zebra_conf

    @property
    def staticd_conf(self):
        """Directory with staticd config files.

        """
        return self._staticd_conf

    @property
    def isisd_conf(self):
        """Directory with isisd config files.

        """
        return self._isisd_conf

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

    def setup(self, net, _topo_dir):
        """Setup the scenario.

        """
        self._reset()
        self._routers_and_hosts(net)


class Plain(Scenario):
    """In a Plain scenario no daemons are run.

    """


class Basic(Scenario):
    """In a Basic scenario, all nodes run zebra, and all hosts run staticd to
    setup a default route.

    """

    def __init__(self):
        Scenario.__init__(self)

    def setup(self, net, topo_dir):
        super(Basic, self).setup(net, topo_dir)

        self._zebra = self._routers.union(self._hosts)
        self._staticd = self._hosts

        self._zebra_conf = os.path.join(topo_dir, "zebra")
        self._staticd_conf = os.path.join(topo_dir, "staticd")


class Isis(Basic):
    """Run IS-IS on all routers.

    """

    def __init__(self):
        Basic.__init__(self)

    def setup(self, net, topo_dir):
        super(Isis, self).setup(net, topo_dir)

        self._isisd = self._routers

        self._isisd_conf = os.path.join(topo_dir, "scenario/isis/isisd")

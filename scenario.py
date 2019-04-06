import importlib
import os


class Scenario(object):
    """Class that describes a network scenario.  A scenario defines which nodes
    are routers and which are hosts as well as which nodes need to start which
    daemons.

    """

    def __init__(self, topology, scenario):
        root_dir = os.path.dirname(os.path.realpath(__file__))

        # Check if the topology directory exists.
        topo_dir = os.path.join(root_dir, "topology/{}".format(topology))
        if not os.path.exists(topo_dir):
            raise KeyError("Topology \"{}\" not supported".format(topology))

        # Extract the topology class.
        self._topo = (importlib
                      .import_module('topology.{}.topo'.format(topology))
                      .NetTopo)

        # Return now if the scenario is "plain".
        if scenario == "plain":
            return

        # Check if the scenario directory exists.  If it does work out which
        # daemons are to be used and on which nodes.  If the scenario is
        # "basic" skip this step.
        if scenario != "basic":
            scenario_dir = os.path.join(topo_dir,
                                        "scenario/{}".format(scenario))
            if not os.path.exists(scenario_dir):
                raise KeyError("Scenario \"{}\" not supported"
                               .format(scenario))

            # Work out which daemons to start and their config directories.
            for daemon in os.listdir(scenario_dir):
                self._get_daemon_nodes(scenario_dir, daemon)

        # Zebra and staticd daemons are special.  If they don't have an
        # override in the scenario directory, take the defaults from the
        # topology directory.
        for daemon in ["zebra", "staticd"]:
            if not hasattr(self, daemon):
                self._get_daemon_nodes(topo_dir, daemon)

    def _get_daemon_nodes(self, parent_dir, daemon):
        # Each daemon entry should be a directory.
        daemon_dir = os.path.join(parent_dir, daemon)
        if os.path.exists(daemon_dir) and os.path.isdir(daemon_dir):
            setattr(self, daemon, set())
            setattr(self, "{}_conf".format(daemon), daemon_dir)

            # Each node running this daemons must have a conf file in the
            # daemon directory called <node_name>.conf.
            for conf in os.listdir(daemon_dir):
                # Make sure we're only dealing with conf files.
                if conf.endswith(".conf"):
                    getattr(self, daemon).add(conf.split('.')[0])

    @property
    def topo(self):
        """The topology of this scenario.

        """
        return self._topo

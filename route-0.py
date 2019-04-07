#!/usr/bin/env python

import argparse
import os

from mininet.net import Mininet
from mininet.cli import CLI

from util.router import Router
from util.experiment import Experiment

FRR_BIN_DIR = "/usr/lib/frr"


def start_daemon(node, daemon, conf_dir):
    """Start one FRR daemon on a given node.

    """
    node.cmd("{bin_dir}/{daemon}"
             " -f {conf_dir}/{node_name}.conf"
             " -d"
             " -i /tmp/{node_name}-{daemon}.pid"
             " > /tmp/{node_name}-{daemon}.out 2>&1"
             .format(bin_dir=FRR_BIN_DIR,
                     daemon=daemon,
                     conf_dir=conf_dir,
                     node_name=node.name))
    node.waitOutput()


def clean():
    """Clean all state left over from a previous experiment.

    """
    os.system("rm -f /tmp/R*.log /tmp/R*.pid /tmp/R*.out")
    os.system("rm -f /tmp/h*.log /tmp/h*.pid /tmp/h*.out")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 {} > /dev/null 2>&1"
              .format(' '.join(os.listdir(FRR_BIN_DIR))))


def run(experiment):
    """Start a network experiment.

    """

    # Clean up any state from previous experiments.
    clean()

    # Start Mininet.
    net = Mininet(topo=experiment.topo(), switch=Router)
    net.start()

    # WARNING: FRR can get confused unless all daemons on each node are started
    #          together.
    for node in net.switches:
        for daemon in experiment.daemons:
            if node.name in getattr(experiment, daemon, set()):
                conf_dir = getattr(experiment, "{}_conf".format(daemon))
                start_daemon(node, daemon, conf_dir)

        if node.name.startswith('R'):
            # Enable IP forwarding
            node.cmd("sysctl -w net.ipv4.ip_forward=1")
            node.waitOutput()

            # Delete spare loopback address for convenience
            node.cmd("ip addr del 127.0.0.1/8 dev lo")
            node.waitOutput()

    CLI(net)
    net.stop()
    os.system("killall -9 {}".format(' '.join(experiment.daemons)))


def main():
    """Route 0 entry point.

    """

    parser = argparse.ArgumentParser(
        description='Launch an FRR network experiment in Mininet.')
    parser.add_argument('--topology', '-t', type=str, required=True,
                        help='the topology of the network')
    parser.add_argument('--scenario', '-s', type=str, required=True,
                        help='the scenario to set up in the network')
    args = parser.parse_args()

    experiment = Experiment(args.topology, args.scenario)

    run(experiment)


if __name__ == "__main__":
    main()

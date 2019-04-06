# Route 0

Route 0 is a suite for learning about and experimenting with routing protocols.
It uses the [Free Range Routing (FRR)](https://frrouting.org/) protocol
implementations running on top of a network setup locally using
[Mininet](http://mininet.org/).

## Introduction

### Motivation

Mininet is a great tool for [teaching, learning, and
experimenting](https://github.com/mininet/mininet/wiki/Teaching-and-Learning-with-Mininet)
with networking.  However, there was no coherent framework or easy to examples
to follow which would let one use Mininet to setup a network running a bunch of
routing protocols.  The FRR project actually uses Mininet for running [topology
tests](https://github.com/FRRouting/frr/tree/master/tests/topotests), but that
makes them difficult to learn from and experiment with.  As somebody looking
for resources to learn about configuring networks to play with on my own
computer that seemed like a big gap.

### Purpose

The primary purpose of Route 0 is to provide a framework for learning how
routing works all the way from setting up IP addresses on individual interfaces
up to setting up BGP peering sessions between multiple autonomous systems and
setting up VPN tunnels.  Therefore, the primary audience are people new to
networking.  However, even if you already know some routing basics you might
still find some of the examples valuable.  The repository is structured such
that you can start from any point you like.

A secondary purpose is to provide an experimental testbed in which a network
running a whole stack of routing protocols can be quickly designed,
provisioned, and brought up on a single computer.

## Getting Started

### Platform

For the best experience it is recommended to run Route 0 experiments using the
Virtual Machine (VM) image developed specifically for this project.

TODO: INSTRUCTIONS FOR VM IMAGE

Note that the VM does not come with the `route-0` repository.  This is because
the repository will be updated much more frequently than the VM image.  You
will still need to clone `route-0` into an appropriate directory on the VM.  To
do so run
```
git clone https://github.com/Wojtek242/route-0.git
```

If you would prefer to set up your own environment, you can follow these
[instructions](platform.md).  They describe the steps needed to produce the
exact same VM image available above.

Note that both Mininet and FRR are developed primarily for Linux so if you have
a different operating system you will have to use some form of virtualisation.
With some effort (and limitations) you might be able to get things running on
other Unix-like systems, but that is undocumented.

### Running an experiment

If you just want to get started, choose a topology from the `topology`
directory, and a scenario from the `scenario` directory within.  Note that all
topologies support `plain` and `basic` in addition the explicit defined
scenarios.  The meaning of these special scenarios is explained later on in
this `README` in the section on scenarios.

Once you have chosen `<topology_name>` and `<scenario_name>` you can run an
experiment with the following command.
```
sudo python route-0.py --topology <topology_name> --scenario <scenario_name>
```

### Lessons

TODO: WRITE UP LESSONS

## Mininet Concepts

This section will introduce some basic Mininet concepts that are in particular
useful for Route 0.  For more information, please refer to the [Mininet
documentation](https://github.com/mininet/mininet/wiki/Documentation).

Mininet is a framework for creating virtual networks running real kernel,
switch, and application code.  In Route 0 it is used to provide the
virtualisation necessary to run multiple routing nodes on a single
computer. Mininet handles the topology setup before dropping the user in its
own special CLI.

The CLI is self-documented and help can be accessed by running `help`.  To
investigate the current topology, you can run `net`.  To visualise the output
of this command, you can copy and paste it into this [web
tool](https://achille.github.io/mininet-dump-visualizer/).

A particularly useful feature of the CLI is the ability to run shell commands
on any of the nodes in the network.  To do this, simply run
```
<node_name> <shell_command>
```
such as `R1 ifconfig`.  This is particularly useful in Route 0 for commands
like `ifconfig` or `ip route`.  Additionally, it is possible to use this
feature to send ping between nodes, for example, `R1 ping 10.0.0.1`.  Normally,
in Mininet the destination can also be specified using its name.  It is
possible to do so in Route 0, but this is often ambiguous as routers will have
multiple IP addresses associated with their interfaces.

## FRR Concepts

This section will introduce some basic FRR concepts that are in particular
useful to understand for Route 0.  For more information, please refer to the
[FRR documentation](http://docs.frrouting.org/en/latest/).

FRR is a set of routing protocols with each running in its own daemon.  In
addition, there is a central IP routing manager, `zebra`, which must be run
before any other routing daemon is started.  All other routing protocols talk
to `zebra` which in turn will talk to the operating system kernel to install
routes as appropriate.

FRR routing protocols are configured using configuration files.  The details of
how to write these configurations are on the [FRR documentation
website](http://docs.frrouting.org/en/latest/).  It is also possible to connect
to running instances of the protocols.  However, this is not currently
supported in Route 0.

TODO: ADD SUPPORT TO CONNECT TO ROUTING PROTOCOL SHELL

## Structure

There are three key concepts in the Route 0 framework: topology, scenario, and
experiment.

### Topology

A topology defines the nodes and links that form the network.  Additionally it
also determines the default IP address assignments and any static routes which
are initialised using the `zebra` and `staticd` daemons.

Each topology has its own directory in the `topology` directory.  Every
topology directory must contain a `topo.py` file which defines a `NetTopo`
class.  The topology itself is defined in the constructor of this class using
the [Mininet API](http://mininet.org/api/classmininet_1_1topo_1_1Topo.html).

A `README.md` should be provided with each topology that has a schematic
diagram of the topology and lists all the default IP address assignments.  It
is assumed that hosts have a default route setup to the router they connect to
and that routers do not have default routes.

### Scenario

A scenario is a particular configuration of FRR daemons on the provided
topology.  While the topology defines which nodes and links form the network,
the scenario determines which daemons get started on which nodes and their
configuration.

There are two special scenarios: `plain` and `basic`. The `plain` scenario
starts the network without any daemons so only the Mininet topology is set up,
but no IP addresses or default routes are created.  The `basic` scenario
additionally starts up `zebra` and `staticd` to configure addresses and default
routes.

Scenarios are defined for a particular topology and thus they can be found in
the `scenario` directory within the topology directories.  There is no python
code associated with a scenario, only FRR configuration files.  Each scenario
(excluding the special ones) should have a directory in the `scenario`
directory.  Within the particular scenario directory, each daemon that is to be
run must have a its own directory.  The configuration files should be created
in the appropriate daemon directory with the name `<node_name>.conf`.

The `zebra` and `staticd` daemons are special and have their own directories
directly in the topology directory.  If a scenario has its own `zebra` and/or
`staticd` directory, these will be used preferentially, but otherwise the
topology's ones will be used.  Note that if no `zebra` and/or `staticd` daemon
is to be run then the scenario must have empty `zebra` and/or `staticd`
directories within its scenario directory.

### Experiment

An experiment is simply a particular topology and scenario combination.
Technically this is redundant since scenarios are strictly associated with only
one topology, but using different terminology avoids confusion.

## Contributing

For information on how to contribute see [CONTRIBUTING](CONTRIBUTING.md).

## Name

I am terrible at coming up with names so I'll at least explain myself.  The
word "Route" was chosen due to its dual meaning.  A route is naturally a
central concept in networking, but it in every day English it simply means a
path, a track, a road.  This repository is a tutorial, a road to learning about
routing protocols, hence a "Route".  The number 0 is used to indicate that this
is the first route one would take in their networking education.


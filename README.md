# Route 0

Route 0 is a suite for learning about and experimenting with routing protocols.
It uses the [Free Range Routing (FRR)](https://frrouting.org/) protocol
implementations running on top of a network setup locally using
[Mininet](http://mininet.org/).

This project was inspired by [Vimal Kumar's BGP hijacking
demo](https://bitbucket.org/jvimal/bgp) from the [Mininet
Wiki](https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo).

## Introduction

### Motivation

Mininet is a great tool for [teaching, learning, and
experimenting](https://github.com/mininet/mininet/wiki/Teaching-and-Learning-with-Mininet)
with networking.  However, there was no coherent framework to use which would
let one use Mininet to setup a network running an entire set of routing
protocols.  A [small example that demonstrated BGP
hijacking](https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo)
has existed for a while and showed that this is possible, but there isn't much
more beyond that on case.

The FRR project actually uses Mininet for running [topology
tests](https://github.com/FRRouting/frr/tree/master/tests/topotests), but that
makes them difficult to learn from and experiment with.  As somebody looking
for resources to learn about configuring networks to play with on my own
computer that seemed like a big gap.

Finally, there are lots of resources online for learning the theory of how
networks are connected to each other and how routing works on the Internet, but
very few of them come with any practical examples.  It is one thing to learn
the concepts and a completely different thing to apply them in a practical real
world scenario.  Route 0 was made to address this issue as well.

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
provisioned, and brought up on a single computer (mostly thanks to Mininet).

## Getting Started

### Platform

For the best experience it is recommended to run Route 0 experiments using the
Virtual Machine (VM) image developed specifically for this project.

1. [Download the ova file](https://drive.google.com/open?id=1safkEvyujpN9liJ9WrCgzbVQTz287C46).
2. In VirtualBox select `File->Import Appliance`, select the downloaded ova
   file and then confirm all the settings.  You may adjust the settings, but
   the defaults will work just fine.
3. Start the Virtual Machine.
4. (Optional) For a better experience install the VirtualBox Guest Additions.
   Instructions on how to do that can be found
   [here](PLATFORM.md#virtualbox-guest-additions).

The account user name is `route0` and the password (needed for sudo commands)
is also `route0`.

If you would prefer to set up your own environment, you can follow these
[instructions](PLATFORM.md).  They describe the steps needed to produce the
exact same VM image available above.

Note that the VM does not come with the `route0` repository.  This is because
the repository will be updated much more frequently than the VM image.  You
will still need to clone `route0` into an appropriate directory on the VM.  To
do so run the following command in a terminal in the VM
```
git clone https://github.com/Wojtek242/route0.git
```

Note that both Mininet and FRR are developed primarily for Linux so if you have
a different operating system you will have to use some form of virtualisation.
With some effort (and limitations) you might be able to get things running on
other Unix-like systems, but that is undocumented.

### Lessons

The lessons in this repository are aimed to take somebody who knows nothing
about IP routing all the way to setting up networks with multiple autonomous
systems and VPN tunnels.  The lessons are structured in such a way that the
reader must first manually setup and configure the network before moving on to
the next step.  Each stage starts at a point that can be automatically
provisioned by Route 0 and the purpose of each lesson is to explain how this
automation is achieved through network configuration.  This particular
structure also means that it is possible to dive in at any point making it
suitable for people with more experience as well.

The table of contents with links to all the lessons can be found in the
[lessons directory](lessons).

### Running an experiment

If you just want to get started, choose a topology from the `topology`
directory, and a scenario from the `scenario` directory within.  Note that all
topologies support `plain` and `basic` in addition to the explicitly defined
scenarios.  The meaning of these special scenarios is explained in the section
on scenarios.

Once you have chosen `<topology_name>` and `<scenario_name>` you can run an
experiment with the following command from the project directory
```
sudo python route0.py --topology <topology_name> --scenario <scenario_name>
```

### Connecting to an FRR daemon

To connect to an FRR daamon, you can either run the following command inside
the Mininet CLI
```
noecho <node_name> telnet localhost <daemon_name>
```

You can also connect to an FRR daemon from a different terminal than the one in
which the Mininet CLI is running.  To do this run
```
sudo python attach.py --node <node_name> --daemon <daemon_name>
```

The password for all daemons is `route0`.

## Mininet Concepts

This section will introduce some basic Mininet concepts that are in particular
useful for Route 0.  For more information, please refer to the [Mininet
documentation](https://github.com/mininet/mininet/wiki/Documentation).

Mininet is a framework for creating virtual networks running real kernel,
switch, and application code.  In Route 0 it is used to provide the
virtualisation necessary to run multiple routing nodes on a single computer.
Mininet handles the topology setup before dropping the user in its own special
CLI.

The CLI is self-documented and help can be accessed by running `help`.  To
investigate the current topology, you can run `net`.  To visualise the output
of this command, you can copy and paste it into this [web
tool](https://achille.github.io/mininet-dump-visualizer/).

A particularly useful feature of the CLI is the ability to run shell commands
on any of the nodes in the network.  To do this, simply run
```
<node_name> <shell_command>
```
such as `R1 ip address`.  This is particularly useful in Route 0 for commands
like `ip address` or `ip route`.  Additionally, it is possible to use this
feature to send pings between nodes, for example, `R1 ping 10.0.0.1`.
Normally, in Mininet the destination can also be specified using its name.  It
is possible to do so in Route 0, but this is often ambiguous as routers will
have multiple IP addresses associated with their interfaces.

It is also possible to launch a shell or run a command in a Mininet node from a
different terminal than the one in which the Mininet CLI is being run.  A
convenience script has been provided for this purpose, `attach.py`.  To launch
a shell on a particular node run
```
sudo python attach.py --node <node_name>
```
You can also directly specify the daemon to connect to with `--daemon` or a
shell command to run with `--cmd`.

The password for all daemons is `route0`.

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
to a shell on running instances of the protocols and configure it from there.
See the Mininet and Getting Started sections on how this can be done.

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

A scenario is a particular configuration of FRR protocols on the provided
topology.  While the topology defines which nodes and links form the network,
the scenario determines which protocols get started on which nodes and their
configuration.

There are two special scenarios: `plain` and `basic`. The `plain` scenario
starts the network without any daemons so only the Mininet topology is set up,
but no IP addresses or default routes are created.  The `basic` scenario
additionally starts up `zebra` and `staticd` to configure addresses and default
routes.

Scenarios are defined for a particular topology and thus they can be found in
the `scenario` directory within the topology directories.  Each scenario
(excluding the special ones) should have a directory in the `scenario`
directory.  Within the particular scenario directory, each daemon that is to be
run must have a its own directory.  The configuration files should be created
in the appropriate daemon directory with the name `<node_name>.conf`.
Scenarios may also have an optional `scenario.py` file for a given scenario in
which a `script` function should be defined.  This function is then run after
Mininet and FRR are started and just before handing control over to the user.

The `zebra` and `staticd` daemons are special and have their own directories
directly in the topology directory.  If a scenario has its own `zebra` and/or
`staticd` directory, these will be used preferentially, but otherwise the
topology's ones will be used.  Note that if no `zebra` and/or `staticd` daemon
is to be run then the scenario must have empty `zebra` and/or `staticd`
directories within its scenario directory.  Note all FRR protocols rely on
`zebra` to function correctly.

### Experiment

An experiment is simply a particular topology and scenario combination.
Technically this is redundant since scenarios are strictly associated with only
one topology, but using different terminology avoids confusion.

### Configuration files

The official FRR documentation recommends using only a single configuration
file `frr.conf` per router.  This makes sense if we are only running a single
instance of each protocol on the device as then all the configuration is in one
place.  Route 0 does not do that.  Using a single configuration file would mean
that a lot of options would need to be repeated between different scenarios,
especially for `zebra` and `staticd`.

Furthermore, separating the config files makes it easier for the python scripts
to know which daemons to start (though of course it could just start all of
them every time or use some additional configuration file).

Finally, one last advantage of the Route 0 configuration model for our use case
is that the we group configurations per protocol, not per device.  This makes
no sense if you're running only one instance of a protocol on a given device,
but since we are running multiple instances on multiple virtual nodes on a
single physical device, it makes it easier to inspect and compare the
configurations on a protocol level.

### End-host configuration files

It's not entirely normal to run FRR daemons on end-hosts.  However, they still
need their IP address and default route configured and the options are to do it
either from a Python script or use FRR daemons.  Using the FRR `zebra` and
`staticd` daemons makes it easier to configure the end-hosts together with the
actual routers.  However, they should not be running any daemon other than
`zebra` and `staticd`.

### A note on VTY shell

The recommended way of connecting to daemons by FRR is to use the [VTY
shell](http://docs.frrouting.org/en/latest/vtysh.html) which can connect to all
the daemons simultaneously.  Unfortunately, in our configuration where multiple
instances of the same daemon run on the same machine in Mininet, it gets
confused and it doesn't connect as expected.  Therefore, you can't use the VTY
shell with Route 0.

## Contributing

For information on how to contribute see [CONTRIBUTING](CONTRIBUTING.md).

## Name

I am terrible at coming up with names so I'll at least explain myself.  The
word "Route" was chosen due to its dual meaning.  A route is naturally a
central concept in networking, but in every day English it simply means a path,
a track, a road.  This repository is a tutorial, a road to learning about
routing protocols, hence it is a "Route".  The number 0 is used to indicate
that this is the first route one would take in their networking education.

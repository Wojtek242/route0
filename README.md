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

If you would prefer to set up your own environment, you can follow these
[instructions](platform.md).  They describe the steps needed to produce the
exact same VM image available above.

Note that both Mininet and FRR are developed primarily for Linux so if you have
a different operating system you will have to use some form of virtualisation.
With some effort (and limitations) you might be able to get things running on
other Unix-like systems, but that is undocumented.

### Running an experiment

### Lessons

## Structure

### Topologies

### Scenarios

## Contributing

There are many ways to contribute to Route 0.  If you are an expert in
networking, you can look for and correct errors, improve the existing lessons,
or add new lessons.  Another way to contribute is to simply add new scenarios
or topologies that you feel would be interesting for others.

### Adding a new topology

Adding a new topology is straightforward.

1. Create a new directory in the `topology` directory.
2. Create a `topo.py` file and define a class `NetTopo` that inherits from
   `mininet.topo.Topo` and build your new topology in its constructor.
3. Create a `zebra` directory and populate it with configuration files for the
   `zebra` daemon to configure the interfaces in your topology.
4. Create a `staticd` directory and populate it with configuration files for
   the `staticd` daemon to configure the default routes on hosts.
5. Create a `README.md` file to describe your topology.

The easiest way to start would be to copy some other topology and customise it
as appropriate.  Once ready, the topology should be automatically detected by
`route-0.py` when you pass your topology's name as the `--topology` argument.

### Adding a new scenario

By default all topologies support the `plain` and `basic` scenarios.  Adding a
additional scenarios is also pretty straightforward.

1. In the topology's directory, make sure there is a `scenario` directory.
   Create one if it doesn't exist.
2. In the `scenario` directory create a new directory for your specific
   scenario.
3. In your new directory create one directory for each daemon you intend to
   run.  You don't need to do this for `zebra` or `staticd` unless you want to
   override the topology defaults.
   
Just like with the topology, the main script should automatically pick up the
new scenario.

## Name

I am terrible at coming up with names so I'll at least explain myself.  The
word "Route" was chosen due to its dual meaning.  A route is naturally a
central concept in networking, but it in every day English it simply means a
path, a track, a road.  This repository is a tutorial, a road to learning about
routing protocols, hence a "Route".  The number 0 is used to indicate that this
is the first route one would take in their networking education.


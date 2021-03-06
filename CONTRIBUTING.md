# Contributing

There are many ways to contribute to Route 0.  If you are an expert in
networking you can look for and correct errors, improve the existing lessons,
add new lessons, or add IPv6 lessons/support.  Another way to contribute is to
simply add new scenarios or topologies that you feel would be interesting for
others and perhaps some accompanying lessons.

## Adding a new topology

Adding a new topology is straightforward.

1. Create a new directory in the `topology` directory.
2. Create an empty `__init__.py` file in the new directory.
3. Create a `topo.py` file and define a class `NetTopo` that inherits from
   `mininet.topo.Topo` and build your new topology in its constructor.
   `WARNING:` Mininet will number the interfaces according to the order they
   are added to a given node.  Make sure the `README.md` reflects this.
4. Create a `zebra` directory and populate it with configuration files for the
   `zebra` daemon to configure the interfaces in your topology.
5. Create a `staticd` directory and populate it with configuration files for
   the `staticd` daemon to configure the default routes on hosts.
6. Create a `README.md` file to describe your topology.

The easiest way to start would be to copy some other topology and customise it
as appropriate.  Once ready, the topology should be automatically detected by
`route0.py` when you pass your topology's name as the `--topology` argument.

## Adding a new scenario

By default all topologies support the `plain` and `basic` scenarios.  Adding a
additional scenarios is also pretty straightforward.

1. In the topology's directory, make sure there is a `scenario` directory.
   Create one if it doesn't exist.  If you had to create the directory, add an
   empty `__init__.py` file to it.
2. In the `scenario` directory create a new directory for your specific
   scenario.  Add an empty `__init__.py` file to it.
3. In your new directory create one directory for each daemon you intend to
   run.  You don't need to do this for `zebra` or `staticd` unless you want to
   override the topology defaults.
   
Just like with the topology, the main script should automatically pick up the
new scenario.


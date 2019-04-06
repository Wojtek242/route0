# Contributing

There are many ways to contribute to Route 0.  If you are an expert in
networking, you can look for and correct errors, improve the existing lessons,
add new lessons, or add IPv6 support.  Another way to contribute is to simply
add new scenarios or topologies that you feel would be interesting for others.

## Adding a new topology

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

## Adding a new scenario

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


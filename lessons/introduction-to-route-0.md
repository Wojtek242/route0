# Introduction to Route 0

This lesson is an introduction to Route 0, some basic networking commands on
Linux, and Wireshark.

## Topology

First, let's look at the topology that we will be using for this lesson, the
`one_rtr` topology.  You can view it in this its
[README](../topology/one_rtr/README.md).  The network is very simple.  It
consists of three nodes, but only one of them, `R1`, is a router, hence the
name of the topology.  The other two are end-hosts.  A host is not necessarily
a different device to a router, but it has a very different role in the
network.  A host will only have one outgoing link and it will not forward IP
packets which means that it can only be the source or destination of IP
communication.  The convention in Route 0 is to name routers with a name that
starts with the letter `R` and hosts with a name starting with `h`.

You can launch the network by running
```
sudo python route0.py --topology one_rtr --scenario basic
```

This command instructs the driver script `route0.py` to start a network with
the `one_rtr` topology running the `basic` scenario.  The `basic` scenario is
special and simply means to run the network and set up all the interface
addresses and default routes.  We will go over what this means later in this
lesson.

Once the CLI prompt appears let us inspect Mininet's representation of the
network by running
```
net
```
in the command prompt.  The output tells us about all the nodes in the network
and the connections between them.  We can see that `R1`'s `R1-eth1` interface
is connected to `h1_1`'s `h1_1-eth1` interface and `R1-eth2` is connected to
`h1_2`'s `h1_2-eth1` interface.  You can visualise the network by copy pasting
the output into this [web
tool](https://achille.github.io/mininet-dump-visualizer/) though its usefulness
is limited for small networks such as this.

## Basic IP commands

Let us now inspect the network using some basic Linux commands.  The three main
commands we will use to investigate the state on the nodes are `ip
address`, `ip route`, and `ping`.  To run any of these commands on a particular node,
you need to prefix it with the node's name in the Mininet CLI.  For example, to
see all the interfaces and their addresses on `R1` you would run
```
R1 ip address
```

There is also an older obsolete command `ifconfig` which is still commonly
used.  However, all information available through `ifconfig` is available
through the `ip` commands.

### ip address

This command lists all addresses assigned to the interfaces on the given
device.  This includes the Ethernet address as well as all IPv4 and IPv6
addresses.  For the purposes of these lessons we are only interested in the
IPv4 addresses which are displayed as either `x.x.x.x` or `x.x.x.x/y`.

The first thing to notice when running this command (especially on `R1`) is
that there are multiple IP addresses assigned to a single device.  This is
because IP addresses are bound to network interfaces not devices.  Furthermore,
it is also possible to assign multiple IP addresses to a single interface.  You
will notice that the `lo` interface on `R1` actually has two IP addresses.

### ip route

The `ip route` command is used to list all the routes installed on a particular
node.  The basic format of a route is `x.x.x.x/y via z.z.z.z` which says that
to reach the IP network `x.x.x.x/y` you must go via the address `z.z.z.z` which
should resolve to a directly connected neighbour.  Note that you won't see such
routes in this network setup, because the network is too simple.

The host nodes have a default route installed which looks like `default via
z.z.z.z` which means that the node should route all traffic it doesn't have a
more specific route for via `z.z.z.z`.

In the network we have running you will also see routes of the form `x.x.x.x/y
dev if-name` which means that in order to reach `x.x.x.x/y` you must go via the
network connected to the interface `if-name`.

### ping

The command `ping` sends a special IP packet to the specified destination to
verify connectivity with that end-host.  Try sending a ping from `h1_1` to an
IP address on `h1_2` by running
```
h1_1 ping 10.2.0.1
```

The address `10.2.0.1` is the IPv4 address assigned to the interface
`h1_2-eth1` on `h1_2`.  The command will keep pinging the specified destination
every second.  To stop press `Ctrl+C`.  Now try pinging the other way.  The
intermediate node `R1` knows how to forward the traffic between the two hosts,
because it is directly connected to both of them.

## Wireshark

Before moving on to the next section it would be good to introduce a
particularly useful tool in studying networks, Wireshark, by using it to look
at pings from `h1_1` to `h1_2`.  Wireshark is a tool that lets you capture and
inspect packets sent and received over all interfaces on a device.
Furthermore, it is able to present them in a human readable form rather than
simply dumping the binary representation directly from the wire.

Start by running the command to trigger `h1_1` to start sending pings to
`h1_2`.  Now open a new terminal window and navigate to the `route0` directory.
We will use the `attach.py` helper script to run Wireshark on `R1` and `h1_2`.
Let's start with `R1` by running
```
sudo python attach.py --node R1 --cmd wireshark
```

When the Wireshark window opens you can dismiss all the Lua errors if you get
any.  First, we need to select which interface we would like to inspect the
packets on.  Let's start with `R1-eth1` as that's the interface that is
connected to `h1_2`, the source of the packets.  You can either double-click on
the interface name or select the appropriate button on the menu bar in the
top-left corner.

Once the packet capture notice how the ping packets appear every second as a
request/reply pair.  Look at the source and destination IP addresses as well.
Note how the originating node has filled out the source address with the
address of its interface `h1_2-eth1` and how the reply has the addresses
flipped around.  Have a look around and inspect the contents if you wish, but
we won't go into any detail on the form of the ping packets.

Now let's look at the packet capture on the other interface on `R1`.  You can
do this by stopping the current capture, finding the capture options button and
starting a capture on `R1-eth2`.  The packets on this interface look identical
which is expected.  The `R1` router has forwarded the request packet from
`R1-eth1` to `R1-eth2` and vice-versa for the reply packet.

You can also inspect the capture on `h1_2`, but since this is a different node
you will have to close the Wireshark window and run the `attach.py` command on
the host node.

## Leaving Route 0

To exit the Mininet CLI and return to the shell just run the `exit` command.
This will shut down all the nodes and protocols that are running.

## Conclusion

In this lesson you learned how to start up Route 0 experiments and learned how
to inspect your network using basic Linux commands and Wireshark.  You will
find these tools will come in handy at all times whenever dealing with
networks.

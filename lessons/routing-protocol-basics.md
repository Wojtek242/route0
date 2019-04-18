# Routing Protocol Basics

In [another lesson](forwarding-between-routers.md) lesson we achieved
connectivity between two hosts by setting up static routes in the network.
This method can work for small networks of a few routers that don't change
much, but would quickly become unmanageable in a larger network, especially if
you want your network to manage failures.  In this lesson we use the same
[simple topology of two routers](../topology/two_rtrs), but this time we set up
the routing protocol IS-IS between the two routers.

## The basics

### Routing vs. forwarding

A common source of confusion is the distinction between routing and forwarding.
Forwarding is the action a router performs to a packet to transfer it from its
input interface to the output interface.  The decision of which output
interface to use is made with the help of a routing table which maps the
destination IP address of a packet to an output interface.  The routing table
can be manually configured just like we did in other lessons or it can be
managed by a routing protocol.

### Routing protocols

A routing protocol manages the communication between the routers in a network
to distribute information about paths to different IP subnets.  It will
automatically discover neighbours, distribute its own connectivity information,
and calculate routes based on information received from its peers.  There are
two ways in which this can be achieved.  In distance vector routing the router
learns about its neighbours' routing tables and builds its own table based on
that information.  This process is referred to as "routing by rumour".  The
alternative is link state routing.  In link state routing each router builds
its internal map of the entire network and calculates the best route based on
this map.  You can read more about their differences
[online](https://techdifferences.com/difference-between-distance-vector-routing-and-link-state-routing.html).

## Setting up a routing protocol

### IS-IS

The routing protocol we will use is IS-IS which is an acronym for Intermediate
System to Intermediate System.  The IS-IS protocol was defined by ISO,
independently of the IETF which defines the TCP/IP protocols, and thus its own
definition and specification is independent of IP and other IETF terminology
and definitions.  For example, "intermediate system" is simply ISO's
nomenclature for router so the name IS-IS simply means router to router.

IS-IS is a link-state routing protocol and it uses Dijkstra's shortest path
algorithm for computing the best paths in the network.

### Start the network

For this lesson we will run the `routing_basics` scenario in the `two_rtrs`
topology

```
sudo python route0.py --topology two_rtrs --scenario routing_basics
```

The `routing_basics` scenario is just the `basic` scenario, but it also starts
the `isisd` daemon on the two routers though it does not configure the
protocol.

Start by inspecting the state of the network using the `ip addr` and `ip route`
commands.  Verify that you are unable to ping `h2_1` from `h1_1` and vice
versa.

Before we start configuring the protocol, let's also open Wireshark to capture
the packets between `R1` and `R2`.  In a separate terminal run

```
sudo python attach.py --node R1 --cmd wireshark
```

We will want to closely inspect what messages the protocol sends to each other
so let's inspect packets on `R1-eth1`.  At first, even though `isisd` is up it
won't be sending any messages.  There may be some other background noise,
notably from ICMPv6 which we can ignore.

### Configuring the IS-IS router

In order to configure the IS-IS protocol, let's connect to its daemon on `R1`.
In a new terminal run

```
sudo python attach.py --node R1 --daemon isisd
```

and enable protocol configuration by running `enable` (password is `route0`
for everything) followed by `configure terminal`.

The first thing we need to do is to configure the IS-IS process.  Currently
only the daemon is running, but the daemon is not running any instances of the
IS-IS protocol so we need to start one.  The first command to run is

```
router isis ROUTE0
```

where `ROUTE0` is simply the name we chose for the IS-IS process.  This drops
us into the `config-router` context in which we adjust the settings for the
process.  We must set a Network Entity Title (NET).  We will set it to
`49.0001.0100.0000.0001.00` with the command

```
net 49.0001.0100.0000.0001.00
```

Since IS-IS was not built exclusively for IP addresses, the NET is not an IP
address.  It is beyond the scope of this lesson to explain the full details of
how to assign a NET, but we will go over the basics.  The first two digits `49`
identify this network as a private network.  Together with the next four
digits, `0001`, they identify the area in the network.  IS-IS has a two level
hierarchy where routers can be assigned to different areas.  The next 12
digits, `0100.0000.0001` are the router ID and it is the binary-coded decimal
form of the router's loopback address.  The last two digits always have to be
`00` to specify that this NET is referring to the current system.

We mentioned that IS-IS has a two level hierarchy.  Level 1 is used for routing
within an area and level 2 is used for inter-area routing.  Our network is too
small to concern ourselves with multiple levels so we will configure our
protocol to use level 2.  We choose level 2 instead of level 1 as this way it
is easier to extend the network in the future to two levels.  To do this we run

```
is-type level-2-only
```

We can now exit the `router` context by running `exit`.

## Adding interfaces

If you now look at the packet capture you will see that nothing has happened
yet even though we just setup a routing process.  The routing protocol isn't
sending any messages, because we haven't told it which interface to include and
use for routing.  Let's add `R1-eth1` as that's the interface connected to
`R2`.  For this we start in the configuration terminal (re-run the commands
from before up to `configure terminal` if your connection timed out) and enter
the interface context

```
interface R1-eth1
```

and we attach this interface to the IS-IS we started in the previous step with

```
ip router isis ROUTE0
```

If you now go to Wireshark you will see IS-IS sending packets!  Specifically,
it will be sending HELLO packets.  HELLO packets are a standard mechanism for
protocols to notify its peers about their presence and hopefully they will hear
a HELLO back.  Currently we only have IS-IS configured on `R1` so the HELLOs
are only sent in one direction.  Have a quick look in Wireshark at what
information is included in the HELLO.

In order to get HELLOs in the other direction we need to repeat the same steps
for `R2`.  The commands are identical, but the NET must be different.  The
router ID must obviously be different, but since we are also running only at
level 2 we need to also assign a different area ID.  A good value for `R2`'s
NET is `49.0002.0100.0000.0002.00`.  Now setup IS-IS on the other side and add
the interface connected to `R1` to the protocol.

Once you finish setting up the other router you will start seeing HELLOs being
sent in both directions (you can tell, because the system ID and source MAC
address are different).  This will allow the protocols to establish so called
adjacencies which simply means they connect with each other and establish some
state for their interactions.

Great! So now we have a routing protocol running on `R1` and `R2` and they're
talking to each other.  Let's try pinging between the hosts.

### Link-State Packets

Unfortunately, as you will find out the two end-hosts still cannot find each
other.  A closer inspection of the routing table on the routers will show that
they haven't actually shared their entire routing tables.  Let's investigate
the Wireshark packet capture to see what they actually are sharing.

IS-IS shares link-state information with other routers using Link-State Packets
(LSPs) so we need to look for those in the packet capture.  Unfortunately, it
doesn't send many of those (as it doesn't need to) compared to the amount of
HELLOs it sends so it may be quite hard to find them manually.  Fortunately,
Wireshark has a filter box at the top and we can simply filter on `isis.lsp`
which will then show us only IS-IS LSPs.  Wireshark's filter mechanism is very
powerful and is worth experimenting with in your own time.

There's a lot of information in these packets, but we can ignore most of it.
Open the `Link State Protocol Data Unit` section and at the bottom there will
be `Extended IP Reachability` (note that not all LSPs will have this so find
those that do).  Expand that group and all groups within.  Here we find all the
IP subnets advertised by the routing protocol.  It shouldn't take too long to
spot the problem now.  Only the `10.0.1.0/24` subnet is being shared which is
the subnet between the two routers.  `R1` and `R2` are not telling each other
about their other interfaces.

At this point you may remember that we only added one interface on each router
to the IS-IS process.  How is the protocol supposed to know which of the other
subnets it needs to advertise?  It could advertise all of the ones it knows
about, but that may be undesirable.  The solution is to instead simply add the
other interface which we want IS-IS to include in its map of the network to the
IS-IS process on each router.  This way the IS-IS process will include that
interface's subnet in its messages as well as any other subnet it learns over
that link.

However, when we added the first interface the router started sending HELLO
packets immediately and in we don't really want that on the link with the hosts.
We just want to add the interfaces for IS-IS to advertise, but we don't want it
to be talking over that link.  To achieve this we simply set the interface to
passive mode.  The commands you need to run on `R1` once you're in the
`configure terminal` are

```
interface R1-eth2
ip router isis ROUTE0
isis passive
```

As soon as you do this you will notice a new LSP in the Wireshark packet
capture and if you inspect its contents you will find the subnet of the
`R1-eth2` interface being advertised.  You should then shortly find that the
`R2` routing table will be updated with this information.  Now make sure to do
apply a similar configuration to `R2` to advertise its path to the connected
host.

Finally, you will start seeing pings between the hosts going through. Success! 

## Configuration files

It is a bit cumbersome to configure everything manually every time we start up
the network.  That is why just like with `zebra` and `staticd` we can configure
`isisd` using configuration files.  The configuration files for the network
configured in this lesson can be found in the [isis
scenario](../topology/two_rtrs/scenario/isis/isisd).  You can find all the
possible options for configuration by either using `?` in the configuration
terminal of `isisd` or by browsing its
[documentation](http://docs.frrouting.org/en/latest/isisd.html).

## Conclusion

In this lesson you have learned how to configure the basics of a routing
protocol, in this case IS-IS, in order to achieve connectivity across a
network.  The network we configured is simple, but it is enough to configure
even more complex networks.  

As an exercise you could try and configure a bigger topology such as the one
[here](../topology/four_areas).  It is up to you if you want to use one or two
levels of IS-IS for it.  An example two-level area division is shown in this
topology's [isis scenario](../topology/four_areas/scenario/isis).  You can try
to configure it manually like the network in this lesson or by using
configuration files.  The solutions are provided in the `isisd` directory of
the scenario, but make sure you try it yourself first.

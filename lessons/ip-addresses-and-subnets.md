# IP Addresses and Subnets

This lesson introduces and explains IP addresses, subnets, and routing between
directly connected devices.

This lesson is a continuation of the
[introduction](introduction-to-route-0.md).  Here, we will manually setup all
the interfaces and routes to achieve the network connectivity we had there for
the `one_rtr` topology.

## Assembling the network

The best way to learn and understand what is going on with addresses and routes
is to actually manually setup the network and inspect the effects of the
individual pieces on the connectivity of the network.

Start the network just like in the introductory lesson, but this time with none
of the address and route configuration by running the `plain` scenario
```
sudo python route0.py --topology one_rtr --scenario plain
```

Start by having a look around using the commands you learned in the previous
lesson, `ip address` and `ip route`, and notice how none of the addresses or
routes are present on any of the nodes.  Furthermore, if you try running the
pings between any of the nodes, you will find they do not work and fail with a
`Network is unreachable error`.  In this lesson we will manually reconstruct
the `basic` network to illustrate all the different concepts involved.

### Assigning IP addresses

A good place to start would be to simply assign all the IP addresses as per the
`one_rtr` topology [README](../topology/one_rtr/README.md).  The command to
assign an IP address to an interface in Linux has the form
```
ip address add [ip]/[mask-digits] dev [if-name]
```

This command assigns the address `ip` associated with the subnet defined by the
`mask-digits` to the interface `if-name`.  This should be pretty
self-explanatory except for the subnet which may be a new concept for some of
you.

An IPv4 address is basically a 32-bit number.  The common representation
`x.x.x.x` simply splits this number into four 8-bit numbers making it more
readable for a human.  This is why none of the four numbers ever exceed 255 as
that is the largest number you can represent with 8 bits.

A subnet is a subdivision of an IP network and determines all the possible IP
addresses that can be connected directly to each other over a local network.
All IP addresses that belong to the same subnet are accessible through the same
local network.  Therefore, having an interface that is part of a particular
subnet means that we can communicate with all the other addresses in that
subnet by using this interface.

The subnet of an IP address is determined by its prefix.  The length in bits of
the prefix is determine by the `mask-digits.`.  Thus, the IP address
`10.11.12.13/24` belongs to a subnet defined by its first 24 bits, that is
`10.11.12.0/24`.  The router will now forward all traffic to any IP address on
this subnet, such as `10.11.12.1` or `10.11.12.165`, over this interface.

This is how in the example in the previous lesson `R1` was able to forward the
packet from `h1_1` to `h1_2`.  `R1` received a packet addressed to `10.2.0.1`
on its interface with `h1_1`.  It quickly determined that `10.2.0.1` belongs to
the subnet `10.2.0.0/24` which is connected to its `R1-eth2` interface which
had the address `10.2.0.254/24`.  Therefore, it was able to forward the packet
over this interface.

Go ahead and assign all the IP addresses to the interfaces in the network.
Don't forget to prefix the commands with the name of the node on which you want
to run the command.

Once all addresses have been assigned try pinging `h1_1` and `h1_2` from the
middle node, `R1`, and verify that this works.  You should also verify that
both `h1_1` and `h1_2` are able to ping the IP address at the other end of
their link.  However, neither `h1_1` or `h1_2` should be able to ping the
interface on the other side of `R1` or each other.

Try also running the `ip route` command on the nodes and notice how they have
the routes associated with the interface subnets installed already without any
additional intervention.

## Address Resolution Protocol (ARP)

In the previous section we said that packets for any address on a given subnet
are forwarded through the interface that belongs to that subnet.  What if the
destination IP address is not connected to that subnet?  In our `one_rtr`
example we only have `10.1.0.1` and `10.1.0.254` on the network on the subnet
`10.1.0.0/24` which is effectively a local network of one point-to-point link.

Try pinging `10.100.0.5` and `10.1.0.5` from `h1_1`.  Notice how both fail, but
only the first one returns the `Network is unreachable error`.  Why does the
second one appear to be stuck?  Since `10.1.0.5` belongs to the same subnet as
`h1_1-eth1` the host tries to send the ping over this interface, but as the
other end does not exist, the response never arrives.

Let's investigate this using Wireshark.  Set up `h1_1` to ping the nonexistent
`10.1.0.5` and open Wireshark on its interface from a different terminal window
by running
```
sudo python attach.py --node h1_1 --cmd wireshark
```
and start a packet capture on the `h1_1-eth1` interface.

The first thing you will notice is how `h1_1` keeps send ARP protocol messages.
ARP stands for the Address Resolution Protocol and is the mechanism by which a
node finds the MAC address of the interface associated with the particular IP
address.  In order to send a packet over a link it must be addressed to the
right MAC address as otherwise no interface on the local network will pick the
packet up.  In this case we see packets constantly asking "Who has 10.1.0.5?
Tell 10.1.0.1", but nobody owns that IP address so nobody responds.

Let's now look at what happens when the IP address exists on the network.  Set
`h1_1` to ping the other end of its link `10.1.0.254` (you don't have to close
wireshark).  Most of the packets sent and received will be the already known
ping packets, but every now and then an ARP request is sent.  However, this
time `h1_1` receives a response telling it the MAC address of the interface.
If you inspect the ping packets that originate at `h1_1` you will notice that
they do use that MAC address in the Ethernet header.

You may wonder why do the nodes need to do this?  After all the IP address
already uniquely identifies the interface.  This is because the IP protocol
doesn't actually know how to communicate over a local network using a physical
interface, it needs another protocol to do it instead.  In this case it's the
Ethernet protocol, but it could be something entirely different such as Wi-Fi
or some older protocol.  The ARP protocol is a tool for the IP protocol to find
out what address to give to the Ethernet protocol so that it can send its
packet to the next node.

## Default routes

At this point `h1_1` and `h1_2` still cannot ping each other.  If you try to
ping `10.2.0.1` from `h1_1` you will be told that the network is unreachable.
If you look at the output of `ip route` on the host this error makes sense.
The routing table doesn't know how to reach any subnet other than
`10.1.0.0/24`.  We could just add a route for the `10.2.0.0/24` subnet to go
via `R1` to `h1_1` which would work for `h1_2`, but would fail as soon as any
new host is added to `R1`.

Instead we will add a default route to our host.  A default route is the route
used for IP addresses that do not match any other more specific route.  To add
a default route we simply run
```
ip route add 0.0.0.0/0 via 10.1.0.254
```
which tells `h1_1` to send all packets via `10.1.0.254` which is the IP address
of the interface on `R1`.  `h1_1` knows how to route to this address, because
it's on the same subnet as its own interface.

Why do we not just install a route to go via the interface directly instead of
specifying an IP address?  In our topology we only have one node connected to
the local network, but in principle we could have more.  In that case,
specifying an interface would not uniquely identify the next hop.

Try pinging `10.2.0.1` from `h1_1` now.  You will notice that it no longer
fails with a "Network unreachable error", but it still doesn't work.  Let's
investigate using Wireshark.  If you inspect the traffic at `h1_1` you will
notice that the requests are being sent, but no responses are received.  Let's
check if `R1` is forwarding the packets.  If you launch Wireshark on `R1` you
will notice that the packets are received on one interface and are forwarded to
the other.  If you also inspect `h1_2` you will find that the request packets
actually manage to make their way to the destination, but no response is sent.

Can you figure out what's going on?  What happens if you try pinging `h1_1`'s
interface from `h1_2`?

The problem is that `h1_2` doesn't have a default route itself.  It receives
the ping packets and it tries to send a response back to source IP address, but
then it finds out it doesn't know how which way to send a packet to that IP
address.  The solution is to install a default route just like we did for
`h1_1`.  Once installed you will notice that pings from `h1_1` now succeed.

## Conclusion

In this lesson you learned how to assign IP addresses to interfaces, what
subnet is and how it is used in routing, and you also learned how to install
default routs on hosts.  With these foundations we can move on to more complex
routing where not all hosts are directly connected to the same router.

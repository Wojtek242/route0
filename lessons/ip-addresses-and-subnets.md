# IP Addresses and Subnets

This lesson introduces and explains IP addresses, subnets, and forwarding
between directly connected devices.  Here, we will manually setup all the
interfaces and routes to achieve network connectivity for the `one_rtr`
topology.  The best way to learn and understand what is going on with addresses
and routes is to actually manually setup the network and inspect the effects of
the individual pieces on the connectivity of the network.

## Starting the network

Start the network as normal using the [`one_rtr` topology](../topology/one_rtr)
and the `plain` scenario

```
sudo python route0.py --topology one_rtr --scenario plain
```

The plain scenario launches the network, but will not set up any addresses or
routes.

Start by having a look around using the commands, `ip addr` and `ip route`, and
notice how no addresses or routes are present on any of the nodes.
Furthermore, if you try running the pings between any of the nodes using the
addresses specified for the [topology](../topology/one_rtr), you will find they
do not work and fail with a `Network is unreachable` error.  In this lesson we
will manually reconstruct this network to illustrate all the different concepts
involved.  The end result will behave just like the `basic` scenario for the
same topology.

## Assigning IP addresses

A good place to start would be to simply assign all the IP addresses as per the
[`one_rtr` topology](../topology/one_rtr).  The command to assign an IP address
to an interface in Linux has the form
```
ip addr add <ip>/<mask-digits> dev <if-name>
```

This command assigns the address `<ip>` associated with the subnet defined by
the `<mask-digits>` to the interface `<if-name>`.  This should be pretty
self-explanatory except for the subnet which may be a new concept.

An IPv4 address is just a 32-bit number.  The common representation `x.x.x.x`
simply splits this number into four 8-bit numbers making it more readable for a
human.  This is why none of the four numbers ever exceed 255 as that is the
largest number you can represent with 8 bits.

A subnet is a subdivision of an IP network and determines a subset of all the
possible IP addresses that can be connected directly to each other over this
subdivision, a local network.  All IP addresses that belong to the same subnet
are accessible through the same local network.  Having an interface that is
part of a particular subnet means that we can communicate with all the other
addresses in that subnet by using this interface.

The subnet of an IP address is determined by its prefix.  The length in bits of
the prefix is determine by the `mask-digits`.  Thus, the IP address
`10.11.12.13/24` belongs to a subnet defined by its first 24 bits,
`10.11.12.0/24`.  The router will now forward all traffic to any IP address on
this subnet, such as `10.11.12.1` or `10.11.12.165`, over this interface.  

This is how in the example in the previous lesson `R1` was able to forward the
packet from `h1_1` to `h1_2`.  `R1` received a packet addressed to `10.2.0.1`
on its interface with `h1_1`.  It was able to then determine that `10.2.0.1`
belongs to the subnet `10.2.0.0/24` which is connected to its `R1-eth2`
interface which had the address `10.2.0.254/24`.  Therefore, it was able to
forward the packet over this interface.

Note that a subnet length does not have to match the 8-bit divisions and
subnets.  `10.11.12.4/30` is also a valid subnet.  Such subnets are very
practical as it allows an operator to assign a more appropriate number of IP
addresses to a particular network than would be otherwise possible.  However,
we will avoid them in these lessons as they are harder to read.

Go ahead and assign all the IP addresses to the interfaces in the network.
Don't forget to prefix the commands with the name of the node on which you want
to run the command.

Once all addresses have been assigned try pinging `h1_1` and `h1_2` from the
middle node, `R1`, and verify that this works.  You should also verify that
both `h1_1` and `h1_2` are able to ping the IP address at the other end of
their link, `10.1.0.254` and `10.2.0.254`.  However, neither `h1_1` or `h1_2`
should be able to ping the other interface on `R1` or each other.

Try also running the `ip route` command on the nodes and notice how they have
the routes associated with the interface subnets installed already without any
additional intervention.  Adding an IP address on a particular subnet on an
interface will automatically add a route to the kernel's routing table that
resolves that particular subnet to that interface.

If you try pinging an IP address that doesn't exist in the network but belongs
to a subnet connected to a local interface, such as `10.1.0.5` from `h1_1`, the
ping won't fail immediately like before.  Instead it will look like it's stuck.
This is because it tries to send the request since it has a routing entry for
the particular subnet, but it isn't getting any replies.

## Address Resolution Protocol (ARP)

Let's investigate this using Wireshark.  Set up `h1_1` to ping the nonexistent
`10.1.0.5` and open Wireshark on its interface from a different terminal window
by running
```
sudo python attach.py --node h1_1 --cmd wireshark
```
and start a packet capture on the `h1_1-eth1` interface.

The first thing you will notice is how `h1_1` keeps sending ARP protocol
messages.  ARP stands for the Address Resolution Protocol and is the mechanism
by which a node finds the MAC address of the interface associated with the
particular IP address.  In order to send a packet over a link it must be
addressed to the right MAC address. Otherwise no interface on the local network
will pick up the packet as they will determine the packet is not addressed for
them.  In this case we see packets constantly asking "Who has 10.1.0.5?  Tell
10.1.0.1", but nobody owns that IP address so nobody responds.

Let's now look at what happens when the IP address exists on the network.  Set
`h1_1` to ping the other end of its link `10.1.0.254` (you don't have to close
Wireshark).  Most of the packets sent and received will be the already known
ping packets, but every now and then an ARP request is sent.  However, this
time `h1_1` receives a response telling it the MAC address of the interface.
If you inspect the ping packets that originate at `h1_1` you will notice that
they will use that MAC address as the destination in the Ethernet header.

You may wonder why do the nodes need to do this?  After all the IP address
already uniquely identifies the interface.  This is because the IP protocol
doesn't actually know how to communicate over a local network using a physical
interface, it needs another protocol to do it instead.  The physical
implementation of the local network may be different for different networks
such as Wi-Fi or Ethernet, but IP is able to run over any of them.  However, in
order to be able to use the physical network protocol it needs to be able to
give it an address that protocol understands and it doesn't understand IP
addresses.  ARP is a tool for IP to find out the physical address to give to
the underlying physical protocol, in this case Ethernet, so that it can send
its packet to the next node.

## Default routes

At this point `h1_1` and `h1_2` still cannot ping each other.  If you try to
ping `10.2.0.1` from `h1_1` you will be told that the network is unreachable.
If you look at the output of `ip route` on the host this error makes sense.
The routing table doesn't know how to reach any destination other than
`10.1.0.0/24`.  The obvious solution is to just add a route for the
`10.2.0.0/24` subnet to go via `R1`.  This would work for `h1_2` on this small
one router network, but would fail as soon as any new host is added to `R1`.

Instead we will add a default route to our host.  A default route is the route
used for IP addresses that do not match any other more specific route.  A host
only has one interface so creating a default route is a pretty straightforward
affair.  To add a default route we simply run

```
ip route add 0.0.0.0/0 via 10.1.0.254
```

which tells `h1_1` to send all packets via `10.1.0.254` which is the IP address
of the interface on `R1` that is connected to `h1_1`.  `h1_1` knows how to
route to this address, because it's connected to the same subnet with
`h1_1-eth1`.

Why do we not just install a route to go via the interface directly instead of
specifying an IP address?  In our topology we only have one node on the other
side of the local network, `R1`, but in principle we could have more.  In that
case, specifying an interface would not uniquely identify the next hop which.

Try pinging `10.2.0.1` from `h1_1` now.  You will notice that it no longer
fails with a `Network is unreachable` error, but it still doesn't work.  Let's
investigate using Wireshark.  If you inspect the traffic at `h1_1` you will
notice that the requests are being sent, but no responses are received.  The
situation is different than when we tried pinging an nonexistent interface,
because we are actually seeing requests being sent.

Let's then check if `R1` is forwarding the packets.  If you launch Wireshark on
`R1` you will notice that the packets are received on one interface and are
forwarded to the other so that can't be it.  If you also inspect `h1_2` you
will find that the request packets do manage to make their way to the
destination, but still no response is sent.

Can you figure out what's going on?  

What happens if you try pinging `h1_1`'s interface from `h1_2`?

The problem is that `h1_2` doesn't have a default route itself.  It receives
the ping packets and it tries to send a response back to the source IP address,
but then it finds out it doesn't know what to do with a packet addressed to
that IP address.  The solution is to install a default route just like we did
for `h1_1`.  Once installed you will notice that pings from `h1_1` now succeed.

## Conclusion

At this point you should have the same network as was for the `basic` scenario.
By building this network manually you learned how to assign IP addresses to
interfaces, what a subnet is and how it is used in routing, and you also
learned how to install default routes on hosts.  With these foundations we can
move on to more complex routing where not all hosts are directly connected to
the same router.

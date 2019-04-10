# Forwarding Between Routers

The `one_rtr` topology is extremely simple and can get away with a lot because
it is directly connected to all the hosts in the network.  Configuring the
subnets on the interfaces is enough to do all the routing it ever needs to do.
What happens when we put one more router in between the two hosts?  This is the
[`two_rtrs` topology](../topology/two_rtrs).  In the `one_rtr` topology,
configuring IP addresses and default routes on the end-hosts by starting the
`basic` scenario was enough for the two hosts to ping each other.  This is not
the case for `two_rtrs`.  In this short lesson we go over the missing link.

## Using Wireshark to find the problem

If you haven't guessed already, Wireshark is often the best tool to use for
debugging any networking problem.  Knowing where exactly your packet was lost
will lead you to the source of the problem much faster.

Start the `two_rtrs` topology in the `basic` scenario

```
sudo python route0.py --topology two_rtrs --scenario basic
```

and get `h1_1` to start sending pings to `h2_1`.  The IP address you want to
ping is `10.2.0.1` which you can verify with the `ip addr` command.  The pings
will fail which is expected.

Now with the help of Wireshark let's trace the steps of the packet and find out
where it is getting lost.  As a reminder you can run Wireshark either directly
from Mininet in the usual way you would run a command on a node or by using the
`attach.py` script in a separate terminal window.

Let's start with node `h1_1` to see if the ping request is being sent at all.
Using the `attach.py`, in a new terminal window we run

```
sudo python attach.py --node h1_1 --cmd wireshark
```

In the Wireshark window we choose the `h1_1-eth1` interface and we see that the
packets are being sent, but no responses being received.  At least we know that
the sender is working fine.

Let's move to the next hop along the path, `R1`.  Close the Wireshark window
and re-open it on `R1`.  Here we have two interfaces to monitor.  From the
[topology](../topology/two_rtrs) file we see that `R1-eth2` is the interface
connected to `h1_1-eth1` so it would be the best place to start.  We quickly
find that this interface is also receiving packets as expected so at least know
there is no fault on the connection between the host and the router.

What do you see if you now move to the other interface on `R1`?  It seems that
our ping requests are being lost somewhere on `R1`.

## Adding a new route

If a router receives packets, but does not forward them it is usually a sign
that something is wrong with the routing table.  Sure enough, if we inspect the
routing table on `R1` using the `ip route` command we find that `R1` does not
know how to reach `10.2.0.1`.  In fact, it even tells `h1_1` about this.  If
you're patient and inspect the packet capture on `R1-eth2` in Wireshark for
long enough you will spot an ICMP response packet notifying about an
unreachable network.  The source address is `R1` interface which shows us that
this error does in fact originate at this router.

The fix is pretty straightforward, we need to add an appropriate route to the
routing table.  But what is an appropriate route?  The end-hosts don't have any
trouble with their routing tables as they have a default route.  A default
route is the route chosen for a packet if there are no other more specific
routes available.  If we install such a default route pointing at `R2` it would
solve our problem, but is this appropriate?  What if we now added one more
router to `R1`?  A default route works for a host, because it only has one
outgoing link, but a router will have multiple links so the choice of a default
route is not such a simple thing to do.

So what route do we install instead?  If you look at `R2`, the route it has
pointing at the `h2_1` host is a route for the `10.2.0.0/24` subnet.
Therefore, we need to tell `R1` to forward all traffic for `10.2.0.0/24` via
`R2`, because that router knows what to do next.  This way when we connect
another router we can simply add a similar route to `R1` for the subnets that
`R3` knows about.  This is in essence what a routing protocol does.  Every node
tells its neighbours which subnets it can reach so that they can install routes
for those subnets pointing at that node.

For a route we also need a next hop which is simply an IP address on the next
router on the path.  We want that next hop to unambiguously point at `R2`.
Therefore, we cannot just point the route at the `R1-eth1` interface as it is
possible to have more than one router connected to that local network.  Instead
we must point the route at the interface on `R2` that is connected to `R1`.
Use `ip addr` or look up the topology file to find this IP address.

Now it is finally time to add the route to `R1`.  The command you need to run
on `R1` is

```
ip route add 10.2.0.0/24 via <next-hop>
```

where you must decide what the `<next-hop>` should be.

Note that installing this route won't immediately solve the ping problem.  You
will find the ping packet to be forwarded correctly, but no response will be
sent.  This is because you must install a similar route on `R2` pointing at the
source subnet of the packets, `10.1.0.0/24` so that the response can also be
forwarded correctly.  It is left to you to figure out how to do this.

Note that if you inspect the packet capture on `R2` before you install that
route you will see that the ping request packets aren't being forwarded to
`h2_1` even though the correct forwarding rules for the forward direction are
installed.  I am not actually sure what is happening, but my guess is that
Linux might not be forwarding packets for which it doesn't recognise the source
address.  This might be a counter-measure to prevent attacks relying on source
IP address spoofing.

## Conclusion

With the reverse route installed you will now be seeing pings succeeding on
`h1_1`.  Success!

In this lesson you learned how to route to subnets on other routers by
installing routes that point at the next router on the path.  This is what
routing protocols do, but in an automated fashion.  To learn how routing
protocols work look out for lessons on configuring IS-IS.

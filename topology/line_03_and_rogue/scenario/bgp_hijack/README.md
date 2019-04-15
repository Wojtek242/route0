# BGP Path Hijacking Attack Demo

This demo is entirely taken from the [Mininet
Wiki](https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo)
and modified to run in Route 0.  All credit for this demo go to the authors of
the Mininet Wiki entry and its [code](https://bitbucket.org/jvimal/bgp).

You can read more about what BGP hijacking is and how the demo works on the
[Mininet
Wiki](https://github.com/mininet/mininet/wiki/BGP-Path-Hijacking-Attack-Demo)
entry.  This `README.md` only adapts the step-by-step instructions from the
Wiki to work with the Route 0 framework.

## Demo Instructions

### Step 1

1. Go into your `route0` repository.
2. Start the `bgp_hijack` scenario with

```
sudo python route0.py --topology line_03_and_rogue --scenario bgp_hijack
```

Keep this shell running throughout this demonstration.

### Step 2

1. In another terminal, let's start a session with AS1's routing daemon:

```
sudo python attach.py --node R1 --daemon bgpd
```

The password is `route0`.

### Step 3

Let's see AS1's routing entries by typing the command `sh ip bgp`.

Notice that on AS1, the chosen AS path to reach 13.0.0.0/8 is "2 3" (i.e., via
AS2 and AS3).

### Step 4

Keep the above shell running in a separate window.  Now, let's visit a default
web server that Mininet started in AS3 and verify that we can reach it from
host h1_1 connected to AS1. We're going to run the command "curl -s 13.0.1.1"
from AS1 in a loop. We have created a script `website.sh` that does this for
you automatically:

```
topology/line_03_and_rogue/scenario/bgp_hijack/website.sh
```

### Step 5

Now, in another window, let us start the rogue AS using the command

```
topology/line_03_and_rogue/scenario/bgp_hijack/start_rogue.sh
```

The rogue AS will connect to AS1 and advertise a route to 13.0.0.0/8 using a
shorter path (i.e., a direct path from AS1 to AS4).  Thus, AS1 will choose this
shorter path by default.

After some time (for BGP convergence), you should see the output of
`website.sh` script change to the attacker's message.

You can also inspect the routing table using the shell you started in step 2.
If the shell closed (due to inactivity), you can start it again (see step 2).
You can see AS4's chosen path and also AS3's path in the routing information
base of AS1.  Since the AS path length to reach 13.0.0.0/8 is smaller through
AS4, R1 chooses AS4 as its next hop.

### Step 6

You can stop the attack by killing R4's routing daemon

```
topology/line_03_and_rogue/scenario/bgp_hijack/stop_rogue.sh
```

You will notice that convergence is quick: the traffic is almost immediately
redirected to the legitimate web server.

### Step 7

You can stop the experiment by typing `exit` at the Mininet prompt, Control-C
in the window where you started the website, and type `exit` in the terminal
where you connected to R1's terminal.

That's it!

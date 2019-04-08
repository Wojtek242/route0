# Configuring Zebra and STATIC

The difference between the `plain` and `basic` scenarios is that the latter
configures interface addresses and default routes on hosts.  In [another
lesson](ip-addresses-and-subnet.md) we used basic Linux commands to build a
`basic` network on top of a `plain` scenario.  However, `route0` does not
implement the `basic` scenario using Linux shell commands.  Instead, it uses
the FRR daemons [Zebra](http://docs.frrouting.org/en/latest/zebra.html) and
[STATIC](http://docs.frrouting.org/en/latest/static.html).

This lesson goes over how to configure Zebra and STATIC to achieve the
connectivity of a `basic` scenario on the [`one_rtr`
topology](../topology/one_rtr).  This is a good way to introduce the basic
usage and configuration of FRR.

If you are only interested in networking concepts and are not interested
learning how to configure FRR daemons you may skip this lesson.

Before you continue with the lesson you may find it useful to read the brief
section on [system architecture on the FRR
website](http://docs.frrouting.org/en/latest/overview.html#system-architecture).

## Starting the daemons

Before we start the network we need to actually create a basic configuration
file that sets the passwords and also raises the loopback interface which we
will use to connect to the daemons.

Create a `route0.conf` file in the root of the project directory with the
following content

```
hostname route0
password route0
enable password route0

interface lo
  no shutdown
```

Now let's start with an empty network

```
sudo python route0.py --topology one_rtr --scenario plain
```

First thing we need to do is launch the daemons.  The two daemons we will use
are `zebra` and `staticd`.  Since all the FRR protocols rely on `zebra` to talk
to the Linux kernel it must always be started first.  There is also a minor
complication due to the fact that these daemons weren't designed to run
multiple instances on a single machine.  The daemons may not work as expected
if you don't start all the daemons on one node before moving to the next one.

To start `<daemon>` on `<node>` we can run the following command in the Mininet
prompt

```
<node> /usr/lib/frr/<daemon> -f route0.conf -d -i $(tempfile).pid
```

Now start the daemons on all the nodes.  Remember that `zebra` must always be
first and start all the daemons on each node before moving to the next one.
Note that since we won't be installing any static routes on `R1` it doesn't
need `staticd`.  You can ignore the message about no kernel support for
MPLS-TE.

## Using Zebra to assign IP addresses

Before we begin, verify that no IP addresses have been assigned on `h1_1` using
the `ip addr` command.  The `lo` interface will have `127.0.0.1/8` assigned to
it, but that IP address is only valid locally and cannot be used for routing.
We need it to connect to the FRR daemons.

Interface IP addresses are assigned using `zebra` so we will first connect to
the `zebra` daemon on `h1_1`.  To do so we will connect using telnet

```
noecho h1_1 telnet localhost zebra
```

`noecho` is just a quirk of the Mininet CLI.  If you don't prefix your command
with `noecho`, you will be seeing double.

You can also connect to the daemon from a separate terminal (the experience is
slightly better as you avoid the Mininet CLI quirks).  In that case, navigate
to the Route 0 directory and run

```
sudo python attach.py --node h1_1 --daemon zebra
```

The password to all the daemons is `route0` just as we set it in the `conf`
file we just created.

Before we start, it is useful to note that if you are ever lost in the FRR
shell, simply press `?` which will list all the commands you can run in the
current context.

The process of assigning an IP address through the `zebra` shell is rather
tedious, but this is because router configuration is a difficult problem.  The
daemon shells follow a configuration model that seems more convoluted than the
basic Linux commands, but that will make sense when configuring much more
complex protocols.

We will go over assigning the IP address for the `h1_1` interface together so
make sure you have connected to the `zebra` daemon on that node.

First we must turn on privileged mode by running (password is `route0` as
usual)

```
enable
```

Next we enter configuration mode

```
configure terminal
```

If you press `?` you will notice that there are lots of things we can configure
at this point.  We are only interested in configuring a specific interface so
we select it.  Note that the terminal has very clever auto-completion
capabilities so try hitting `<tab>` after typing just a few letters.

```
interface h1_1-eth1
```

Finally, we are at a point where we can add an IP address

```
ip address 10.1.0.1/24
```

Now let's exit the `zebra` shell.  Run `exit` as many times as you need until
you're back in the Mininet prompt if you connected from Mininet (careful not to
exit Mininet or you will have to redo all of this!) or your default shell if
you connected from a different terminal using `attach.py`.  If you now run
`h1_1 ip addr` you will see the IP address on the interface!

The `zebra` shell is used for more than just configuration.  It can also give
you a lot of information about the system's state.  Connect to the `zebra`
daemon on `h1_1` once again.  This time we will inspect the `show` command.
Try running the following commands in the shell and inspect their output

```
show interface
show interface h1_1-eth1
show ip route
```

As you can see we can get a lot of nicely formatted state information this
way.  We haven't seen anything we can't find out using basic Linux commands,
but that's because we haven't done anything complicated yet.  Feel free to
explore the `zebra` daemon more by pressing `?` whenever you can.

When you finish exploring the daemon, assign all the other IP addresses as
shown in the [topology](../topology/one_rtr).

Verify what you've done by pinging the IP addresses on `h1_1` and `h1_2` from
`R1`.

## Using STATIC to create static routes

In order to complete the network we need to create default routes on the
hosts.  The hosts have only one outgoing link so it makes sense they have a
rule which says to send all traffic over this link.

If you try to connect to `staticd` from Mininet using the same method as for
`zebra` it will fail.  This is because Linux doesn't know the port number of
`staticd` (presumably as it's a newer daemon).  Therefore, if you want to
connect from the Mininet prompt you need to use the port number, `2616`,
explicitly

```
noecho h1_1 telnet localhost 2616
```

Note that if you use the `attach.py` script from a separate terminal window,
you can still just use the name `staticd`.

Connect to the `staticd` daemon on `h1_1`, enable privileged mode, and enter
the configuration terminal.  Once in the configuration terminal we can create
the default route.  Can you figure out the right command using `?`?. Hint: do
not use the `via` word.

The full command to install a default route on `h1_1` is

```
ip route 0.0.0.0/0 10.1.0.254
```

which is very similar to the Linux command you would run for the same effect.
If you exit the daemon's shell you can now check that your route installed
correctly using `ip route`.  Repeat the process for `h1_2`.

When you finish you can verify that everything is correctly set up by checking
whether `h1_1` can ping the interface IP address on `h1_2` and vice versa.

If the ping succeeds, congratulations on configuring your first network using
the FRR daemons!

## Configuring the protocols using configuration files

The manual configuration process was rather tedious which is why configuration
files exist.  When you start the network in the `basic` scenario using
`route0.py` it simply reads in a bunch of configuration files.  The ones it
reads on for `one_rtr` can be found in the
[`staticd`](../topology/one_rtr/staticd) and
[`zebra`](../topology/one_rtr/zebra) directories in its [topology
directory](../topology/one_rtr).  Have a look at them and see how similar they
are to the commands we have just run to configure the network.

## Conclusion

In this lesson you learned how to configure a `basic` scenario on the `one_rtr`
network.  You learned how to connect to the FRR daemons, how use them for
configuration and displaying routing state.  You also tried exploring the
different options available in the shell using `?`.  All these skills will be
useful when configuring actual routing protocols in later lessons.


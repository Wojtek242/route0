# Platform

Route 0 is developed and officially supported only on Ubuntu 18.04 using the
distribution provided `mininet` package (version 2.2.2) and FRR Stable
installed from the FRR [debian repositories](https://deb.frrouting.org/).  It
is almost certain that everything will work on any other Linux distribution
with a sufficiently up to date kernel, Mininet, and FRR installation, but this
has not been tested.  For kernel compatibility please refer to the [FRR
website](http://docs.frrouting.org/en/latest/overview.html#supported-protocols-vs-platform).

## Setting up a Virtual Machine

The following instructions setup exactly the same VM that is suggested in the
 main `README` file.  The instructions are provided below if for some reason
 you would prefer not to or are not able to use the pre-configured image.

### Base Operating System

For the base OS, the VM uses Xubuntu 18.04.  Version 18.04, because it's the
most recent LTS version and more importantly it comes with kernel version 4.18
which is new enough for all the FRR features.  The XFCE spin was chosen as a
GUI is helpful for wireshark as well as people unfamiliar with Linux.  XFCE is
a lightweight yet fully featured desktop environment.

You can download a Xubuntu 18.04 ISO image from the [official
website](https://xubuntu.org/download).

Install the OS in the virtualisation system of your choice.  If you're not
familiar with virtualisation systems, the easiest one to use and that is
supported on all major operating systems is
[VirtualBox](https://www.virtualbox.org/).

After the installation completes, install all updates.  Xubuntu should prompt
you to do so shortly after the first boot, but you can also do it manually from
a terminal with the following command lines:

```
sudo apt update
sudo apt upgrade
```

Once the system finishes updating, I strongly recommend uninstalling
`unattended-upgrades` as they have been known to cause problems inside virtual
machines, especially with VirtualBox Guest Additions installed.  To do so, open
the terminal and run the following command

```
sudo apt purge unattended-upgrades
```

### VirtualBox Guest Additions

If you are using VirtualBox, you may find it useful to install the VirtualBox
Guest Additions.  Note that these are not actually included in the provided VM
image as the installation depends on the VirtualBox version in use.

The best way to install the guest additions is to install them from the ISO
image provided by VirtualBox.  Before doing that though, you need to first
install `dkms` and `build-essential`.  In the terminal inside the VM run

```
sudo apt install dkms build-essential
```

Now you need to obtain the CD.  Open your VM and from the menu bar select
`Devices->Insert Guest Additions CD image`.  This will download the image.

In case the download fails, you can download the image directly from the
[VirtualBox website](http://download.virtualbox.org/virtualbox/).  Make sure
you choose the right version for your VirtualBox installation (you can find it
from the menu bar `Help->About VirtualBox`) and download the
`VBoxGuestAdditions_<version>.iso`.  Once the download completes make sure to
mount it in the settings window of your virtual machine.

Open the file explorer in the VM and navigate to the inserted CD.  From here
right click and select `Open Terminal Here`.  The last step is now to run

```
sudo ./VBoxLinuxAdditions.run
```

Once the installation completes, reboot the VM.  Amongst other things you can
now enable the shared clipboard from the menu bar with `Devices->Shared
Clipboard`.

### Installing Mininet

Mininet is available from the Ubuntu repositories.  Simply run

```
sudo apt install mininet
```

It is also useful to install some other components for use with Mininet such as
wireshark.  You can do that manually or use the Mininet script provided for
this purpose.  You will need `git` installed for this.  If you already have
`git` installed you can skip the first line

```
sudo apt install git
git clone git://github.com/mininet/mininet
mininet/util/install.sh -fw
```

### Installing FRR

Installing FRR is also easy on Ubuntu as the developers maintain a Debian
repository which can be used for Ubuntu as well.  To install FRR from this
repository, install curl first

```
sudo apt install curl
```

and follow [these instructions](https://deb.frrouting.org/).

### Additional tools

The above instructions will miss some useful tools which are good to have when
building and troubleshooting networks.  To install them run

```
sudo apt install traceroute
```

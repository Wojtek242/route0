"""Script to launch web servers for the BGP hijack demo."""

import os


def script(net):
    """The script."""

    # Clean up after any previous experiment.
    os.system('pgrep -f webserver.py | xargs kill -9')

    # Start honest server.
    net.getNodeByName("h3_1") \
       .popen("python"
              " topology/line_03_and_rogue/scenario/bgp_hijack/webserver.py"
              " --text 'Default web server'", shell=True)

    # Start rogue server
    net.getNodeByName("h4_1") \
       .popen("python"
              " topology/line_03_and_rogue/scenario/bgp_hijack/webserver.py"
              " --text '*** Attacker web server ***'", shell=True)

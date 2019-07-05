import sys
from launchmodes import QuietPortableLauncher, PortableLauncher

numclients = 8


def start(cmdline):
    # PortableLauncher(cmdline, cmdline)()
    QuietPortableLauncher(cmdline, cmdline)()

# start('echo_server.py')                # spawn server locally if not yet started
# args = ' '.join(sys.argv[1:])          # pass server name if running remotely
where = sys.argv[1]
args = ' '.join(sys.argv[2:])
for i in range(numclients):
    start('echo_client.py %s %s' % (where, args))    # spawn 8? clients to test the server

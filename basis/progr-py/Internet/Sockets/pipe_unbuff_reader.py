# no output for 10 seconds unless python -u flag used or sys.stdout.flush()
# but writer's output appears here every 2 seconds when either option is used

import os

for line in os.popen('python -u pipe_unbuff_writer.py'):
    print(line, end='')     # blocks without -u!

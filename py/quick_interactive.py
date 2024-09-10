import subprocess
import re
import os
import sys

# Get qstat output
res = subprocess.run(['qstat'], stdout=subprocess.PIPE).stdout.decode('utf-8')

# Parse result into tasks
tasks = res.split('\n')[2:-1]
for task in tasks:
    status = task.split()

    # Identify interactive task
    if status[1] != 'STDIN':
        continue

    # query task server hostname
    jobid = status[0]
    print(f'"{jobid}" identified.')

    qps = subprocess.run(['qps', jobid], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')
    m = re.search(r'\((gadi-.*)\)', qps)
    
    if m is None:
        sys.stderr.write(f'Unable to parse qbs output\n')
        sys.stderr.write(qps)

    hostname = m.group(1)
    print(f'ssh {hostname}')
    os.system(f'ssh {hostname}')

    exit(0)

sys.stderr.write('No interactive task found!\n')
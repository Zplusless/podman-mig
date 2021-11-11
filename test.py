
from call_cmd import cmd_run

script = 'cd /ga/bin \nsed -i \"s/:0/$(echo $DISPLAY)/\" config/common/server-common.conf \n./ga-server-periodic config/server.desktop.conf\n'
cmd_run(f'mkdir /tmp/podman/ga', True)
with open('/tmp/podman/ga/run_ga.sh', 'w') as f:
    f.write(script)

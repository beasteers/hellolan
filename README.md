# hellolan
Intuitive port scanning! This module is just a couple functions that wrap nmap and are exposed as command line tools.

Basically, I made this because I often need to scan for raspberry pi's on my local network and was always frustrated about remembering the correct commands. Then I needed to do some automated scanning in Python, so I just wrapped it all up in a few python functions with a cli.

## Install

```bash
pip install hellolan
```

## Usage

```bash
# by default, we scan ports 21-443
hellolan scan

# there are some presets too
hellolan ssh # --port=22
hellolan web # --port=80,443
```
Example output:
```
$ hellolan ssh
hostname           ip             ports
-----------------  -------------  -------
                   192.168.1.127  [22]
node-b827e9j315hf  192.168.1.236  [22]
-
Took 3.3 seconds
```

There's more:
```bash
# you can filter the results too
hellolan ssh hostiwant # match an exact hostname
hellolan ssh 'host*' --ignore='badhost-*' # matching glob
hellolan ssh 192.168.1.84 # match an exact ip
# NOTE: lmk if you'd prefer regex over fnmatch

# you can change the net hosts to scan.
# by default --net=192.168.1.0/24
# so it's not exclusively for lan ...!! helloevbody!
hellolan scan --net=scanme.nmap.org
hellolan scan --net=198.116.0-255.1-127
hellolan scan --net=216.163.128.20/20

# you can also poll localhost:
# here I'm checking what I have for jupyter lab instances running.
# they autoincrement ports as 8888 + i. I'm assuming I don't have
# more than 7.
hellolan scan --net=localhost --ports=8888-8893
# Outputs:
#     hostname    ip         ports
#     ----------  ---------  ------------
#     localhost   127.0.0.1  [8888, 8889]
#     -
#     Took 11.4 seconds
```

#### It's also importable!

```python
import hellolan

for d in hellolan.scan(ports='21-22'):
    print('{hostname} ({ip}) - {ports}'.format(**d))
```

## Notes
 - this uses the default `nmap.PortScanner().scan(host, ports=ports)` setup. I'm not sure I'm knowledgeable enough to pick better defaults, but there may be ways to speed it up.

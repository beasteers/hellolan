# hellolan
Intuitive port scanning! This module is just a couple functions that wrap nmap and are exposed as command line tools.

Basically, I made this because I often need to scan for raspberry pi's on my local network and was always frustrated about remembering the correct commands. Then I needed to do some automated scanning in Python, so I just wrapped it all up in a few python functions with a cli.

## Install

```bash
# mac
brew install nmap
# linux
apt-get install nmap

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

If you run with `sudo`, you can also see the mac address and vendor.

```
$ sudo hellolan ssh --watch
hostname                ip             ports    mac                vendor
----------------------  -------------  -------  -----------------  ---------------------------

raspberrypi  192.168.1.242  [22]     DC:A6:32:C4:F4:A3  Raspberry Pi Trading
raspberrypi  192.168.1.65   [22]     DC:A6:32:A9:F0:82  Raspberry Pi Trading
             192.168.1.66   [22]     52:D4:F7:18:5F:74
             192.168.1.67   [22]     00:1A:62:03:F3:FF  Data Robotics, Incorporated
Scan 1 finished at Tue Jan 19 23:08:55 2021. took 10.2s. Found 4 hosts.
```


There's more:
```bash
# you can filter the results too
hellolan ssh node- # match a partial hostname
hellolan ssh 'host*' --ignore='badhost-*' # matching glob
hellolan ssh 192.168.1.84 # match an exact ip
# NOTE: lmk if you'd prefer regex over fnmatch

# you can change the net hosts to scan.
# by default it's the local router subnet --net=192.168.1.0/24
# so it's not exclusively for lan ...!! helloevbody!
hellolan scan --net=scanme.nmap.org
hellolan scan --net=198.116.0-255.1-127
hellolan scan --net=216.163.128.20/20

# you can also poll localhost:
# here I'm checking what I have for jupyter lab instances running.
# they autoincrement ports as 8888 + i. I'm assuming I don't have
# more than 7.
hellolan scan --net=localhost --port=8888-8893
# Outputs:
#     hostname    ip         ports
#     ----------  ---------  ------------
#     localhost   127.0.0.1  [8888, 8889]
#     -
#     Took 11.4 seconds
```

You can print it out in more parseable formats
```bash
$ hellolan ssh -ip
# 192.168.1.127
# 192.168.1.236
$ hellolan ssh -ip -json
# ["192.168.1.127", "192.168.1.236"]
$ hellolan ssh -json
# [{"hostname": "", "ip": "192.168.1.127", "ports": [22]}, {"hostname": "raspberrypi", "ip": "192.168.1.236", "ports": [22]}]
```

#### Now you can use the command to directly ssh into a device !!!
How it works - it will split by the '@' symbol, poll for a device who's host matches 'abc' and replaces 'abc' with the found ip address.
```bash
hellolan ssh- user@abc
```
So for example:
```bash
mbp $ hellolan ssh- user@abc
#
# Multiple hosts found:
#     hostname  ip             ports
# --  --------  -------------  -------
#  0  abcdejkl  192.168.1.127  [22]
#  1  abcdefgh  192.168.1.236  [22]
#
# Which host to use? [0]: >> 1
# Using host: abcdefgh
#
# ---------------------
# Starting SSH Session: $ ssh sonyc@192.168.1.236
# ---------------------
#
# Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
# permitted by applicable law.
# Last login: Wed Apr 15 18:40:32 2020 from 192.168.1.214
user@abcdefgh:~ $ hostname
abcdefgh
user@abcdefgh:~ $ exit
logout
Connection to 192.168.1.236 closed.
#
# -------------------
# Ended SSH Session. (ssh sonyc@192.168.1.236)
# -------------------
#
mbp $
```

#### It's also importable!

```python
import hellolan

for d in hellolan.scan(port='21-22'):
    print('{hostname} ({ip}) - {ports}'.format(**d))
```

## Notes
 - this uses the default `nmap.PortScanner().scan(host, ports=ports)` setup. I'm not sure I'm knowledgeable enough to pick better defaults, but there may be ways to speed it up.

 - Update: after playing around with settings, there are indeed ways of speeding it up.
    - I made version checking optional. nmap.PortScanner.scan does version checking by default (`-sV`). I removed that and now you can re-enable it using `--services`. I haven't seen any lost information and the queries are now waaaay faster.
    - if you are trying to speed up `--services`, you can specify version intensity (`--intensity 0-9`) with `0` using fewer checks (faster) and `9` using the most (comprehensive). I noticed significant decrease in runtime when using `--services` with `--intensity 0`
    - You can specify how many of the top ports to use (default is `--top 200`), fewer is faster, (nmap default is `1000`).

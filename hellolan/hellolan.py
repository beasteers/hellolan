import fnmatch
import nmap
import logging

log = logging.getLogger(__name__)

nm = nmap.PortScanner()

def lanscan(net='192.168.1.0/24', ports='22-443'):
    '''Scan network and ports.

    ports='22-433', ports=22, ports='22,80', ports=(80, 443, '2000-2200')
    '''
    if isinstance(ports, (tuple, list)):
        ports = ','.join(map(str, ports))

    nm.scan(net, ports=str(ports))
    for host in nm.all_hosts():
        ports = [
            port for proto in nm[host].all_protocols()
            for port, status in nm[host][proto].items()
            if status['state'] == 'open']

        if ports:
            yield {
                'hostname': nm[host].hostname(),
                'ip': host, 'ports': ports}


def scan(hostname=None, ignore=None, ip=None, n=None, hasname=None, **kw):
    '''Scan devices on your local network. Filter by hostname or ip.
    '''
    # get all devices
    devices = lanscan(**kw)
    if hostname:
        devices = (d for d in devices if matches(d, hostname))
    if ignore:
        devices = (d for d in devices if not matches(d, ignore))
    if ip:
        devices = (d for d in devices if check_ranges([d['ip'], d['ip'].split('.')], ip))
    if hasname:
        devices = (d for d in devices if d['hostname'])
    if n is not None:
        devices = (d for d, i in zip(devices, range(n)))
    # get devices grouped into different categories
    return devices


'''

Utils

'''

MATCH_COLS = 'hostname', 'ip'
matches = lambda d, pat: any(
    pat in d[c] or fnmatch.fnmatch(d[c], pat) for c in MATCH_COLS)

def check_ranges(xs, ranges):
    ranges = str(ranges).split(',')
    between = lambda x, xmin, xmax: xmin < x < xmax
    return any(
        (between(x, *r.split('-')) if '-' in r else x == r)
        for x in xs for r in ranges
    )

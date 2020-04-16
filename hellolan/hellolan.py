import fnmatch
import nmap
import logging

log = logging.getLogger(__name__)

nm = nmap.PortScanner()

def lanscan(net='192.168.1.0/24', port=None, intensity=None,
            nmapargs=None, top=200, services=False):
    '''Scan network and ports.

    port='22-433', port=22, port='22,80', port=(80, 443, '2000-2200')
    '''
    if isinstance(port, (tuple, list)):
        port = ','.join(map(str, port))

    nmapargs = (nmapargs,) if isinstance(nmapargs, str) else tuple(nmapargs or ())
    if services:
        nmapargs = ('-sV',)
    if intensity is not None:
        assert 0 <= intensity <= 9
        nmapargs += ('--version-intensity {}'.format(intensity),)
    if top:
        nmapargs += ('--top-ports {}'.format(top),) #('-F',) # -F is not working

    nm.scan(net, ports=str(port) if port else None, arguments=' '.join(nmapargs))
    for host in nm.all_hosts():
        ports = [
            port for proto in nm[host].all_protocols()
            for port, status in nm[host][proto].items()
            if status['state'] == 'open']

        if ports:
            yield {
                'hostname': nm[host].hostname() or '',
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

def matches(d, pat):
    pat = str(pat)
    return any(pat in d[c] or fnmatch.fnmatch(d[c], pat) for c in MATCH_COLS)

def check_ranges(xs, ranges):
    ranges = str(ranges).split(',')
    between = lambda x, xmin, xmax: xmin < x < xmax
    return any(
        (between(x, *r.split('-')) if '-' in r else x == r)
        for x in xs or () for r in ranges
    )

from . import scan


def ssh_into(hostname, *a, user=None, i=None, sshargs=None, port=None, **kw):
    '''ssh into a host by hostname'''
    from subprocess import call

    hostname, user, port = _parse_hostname(hostname, user, port)
    hosts = list(scan(hostname, *a, port=port or 22, **kw))
    host = _resolve_multiple_hosts(hosts, i)

    if not host:
        return

    cmd = 'ssh {} {}'.format(_build_hoststr(host['ip'], user, port), sshargs or '').strip()

    print('''
---------------------
Starting SSH Session: $ {cmd}
---------------------
'''.format(cmd=cmd))
    call(cmd, shell=True)
    print('''
-------------------
Ended SSH Session. ({cmd})
-------------------
'''.format(cmd=cmd))




def _parse_hostname(hostname, user=None, port=None):
    if not user:
        user, hostname = hostname.split('@') if '@' in hostname else (hostname, None)
    if not port:
        hostname, port = hostname.split(':') if ':' in hostname else (hostname, None)
    return hostname, user, port

def _build_hoststr(hostname, user, port):
    if user:
        hostname = '{}@{}'.format(user, hostname)
    if port:
        hostname = '{} -p {}'.format(hostname, port)
    return hostname

def _resolve_multiple_hosts(hosts, i=None):
    print()
    # select which host to connect to
    if not hosts:
        print('No hosts found.')
        return

    if len(hosts) > 1: # by default, ask for multiple
        from tabulate import tabulate
        print('Multiple hosts found:')
        print(tabulate(hosts, headers='keys', showindex=True))
        print()

        if i is None:
            i = int(input('Which host to use? [0]: ').strip() or 0)
    else:
        i = 0

    host = hosts[i or 0]
    print('Using host: {}'.format(host['hostname']))
    return host

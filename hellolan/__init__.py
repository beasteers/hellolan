from functools import wraps
from .hellolan import *
from .ssh import *

PRESETS = {
    'ssh': 22, 'web': '80,443',
}

def main():
    '''Hellolan CLI'''
    import fire
    fire.Fire({
        'get': partial(getall, n=1),
        'getall': getall,
        'scan': _gentable(scan),
        **{k: _gentable(get_preset(k)) for k in PRESETS},
        'ssh-': ssh_into,
        'hostname': hostname,
    })

def ssh_main():
    '''SSH Into CLI'''
    import fire
    fire.Fire(ssh_into)


def getall(col, hostname=None, preset=None, *a, **kw):
    return [d[col] for d in get_preset(preset)(hostname, *a, **kw)]


def get_preset(name):
    if name not in PRESETS:
        return scan
    kw = PRESETS[name]
    return partial(scan, **(kw if isinstance(kw, dict) else {'port': kw}))


def _loop(n):
    if n:
        yield from range(n)
    else:
        while True:
            yield

def _dict_update(prev, new):
    prev, new = prev or {}, new or {}
    return dict(prev, **{k: new[k] or prev.get(k) for k in new})

def _dict_drop(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}

def _gentable(func):
    '''Will print out rows of a table as they are generated by func(*a, **kw).
    I've found out that it's not super necessary because nmap.PortScanner
    yields most things toward the end anyways. So I may end up removing reprint.
    '''
    import time
    import functools
    import itertools
    from tabulate import tabulate

    def table(items, headers=None, sortby=None):
        if isinstance(items, dict):
            items = list(items.values())
        if not headers and items and isinstance(items[0], dict):
            headers = 'keys'
        if sortby:
            items = sorted(items, key=lambda x: x[sortby])
        return tabulate(items, headers=headers or ())

    def allatonce(*a, headers=None, **kw):
        data = list(func(*a, **kw))
        print(table(data, headers))
        return data

    def asavailable(*a, headers=None, times=None, **kw):
        import datetime
        import reprint
        items = {}
        try:
            with reprint.output() as out:
                out.append('Starting scan...')
                for i in _loop(times):
                    t0 = time.time()
                    for x in func(*a, **kw):
                        items[x['ip']] = _dict_update(items.get(x['ip']), x)
                        out.change(table(items, headers).splitlines())
                        out.append('Scan finished at {}. took {:.1f}s. Found {} hosts.'.format(
                            datetime.datetime.now().strftime('%c'), time.time() - t0, len(items)))
        except KeyboardInterrupt:
            print('\nInterrupted.')
        return list(items.values())

    def parseable(*a, headers=None, **kw):
        data = list(func(*a, **kw))
        headers = headers or set().union(d.keys() for d in data)
        print('\n'.join([
            '\t'.join([d.get(c) or '' for c in headers])
            for d in data
        ]))
        return data

    def as_json(*a, headers=None, **kw):
        import json
        data = list(func(*a, **kw))
        headers = headers or len(data) and data[0].keys() or ()
        data = ([d[headers[0]] for d in data] if len(headers) == 1 else
                [{c: d[c] for c in headers} for d in data])
        print(json.dumps(data))
        return data

    def save_json(out, result):
        import json
        with open(out, 'w') as f:
            json.dump({
                d['ip']: _dict_drop(d, 'ip', 'ports') for d in result
            }, f)

    @functools.wraps(func)
    def inner(*a, headers=None, ip=False, watch=False, tab=False, timer=True, json=False, out=None, **kw):
        t0 = time.time()
        if ip:
            headers, tab = ('ip',), True
        if watch:
            result = asavailable(*a, headers=headers, **kw)
        elif json:
            result = as_json(*a, headers=headers, **kw)
        elif tab:
            result = parseable(*a, headers=headers, **kw)
        else:
            result = allatonce(*a, headers=headers, **kw)
        if out:
            save_json(out, result)
        if timer and not tab and not json:
            print('-')
            print('Took {:.1f} seconds'.format(time.time() - t0))
    return inner

def partial(func, *a, **kw):
    '''functools.partial doesn't apply wraps ???? wtf ??? it's right there......'''
    return wraps(func)(lambda *ai, **kwi: func(*a, *ai, **kw, **kwi))


if __name__ == '__main__':
    main()

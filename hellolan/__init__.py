from functools import wraps
from .hellolan import *

PRESETS = {
    'ssh': 22, 'web': '80,443',
}

def main():
    import fire
    fire.Fire({
        'get': _wrap(getall, n=1),
        'getall': getall,
        'scan': _gentable(scan),
        **{k: _gentable(get_preset(k)) for k in PRESETS},
    })


def getall(col, hostname=None, preset=None, *a, **kw):
    return [d[col] for d in get_preset(preset)(hostname, *a, **kw)]


def _wrap(func, *a, **kw):
    '''functools.partial doesn't apply wraps ???? wtf ???
    it's right there......'''
    return wraps(func)(
        lambda *ai, **kwi: func(*a, *ai, **kw, **kwi))


def get_preset(name):
    if name not in PRESETS:
        return scan
    kw = PRESETS[name]
    return _wrap(scan, **(kw if isinstance(kw, dict) else {'ports': kw}))

def _gentable(func):
    '''Will print out rows of a table as they are generated by func(*a, **kw).
    I've found out that it's not super necessary because nmap.PortScanner
    yields most things toward the end anyways. So I may end up removing reprint.
    '''
    import time
    import functools
    from tabulate import tabulate

    def table(items, headers=None):
        if not headers and items and isinstance(items[0], dict):
            headers = 'keys'
        return tabulate(items, headers=headers or ())

    def allatonce(*a, headers=None, **kw):
        print(table(list(func(*a, **kw)), headers))

    def asavailable(*a, headers=None, **kw):
        import reprint
        with reprint.output(interval=0.3) as out:
            items = []
            for x in func(*a, **kw):
                items.append(x)
                out.change(table(items, headers).splitlines())

    @functools.wraps(func)
    def inner(*a, headers=None, timer=True, **kw):
        t0 = time.time()
        # asavailable(*a, headers=headers, **kw)
        allatonce(*a, headers=headers, **kw)
        if timer:
            print('-')
            print('Took {:.1f} seconds'.format(time.time() - t0))
    return inner




if __name__ == '__main__':
    main()

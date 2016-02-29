from __future__ import absolute_import, print_function

import functools
import itertools
import time


def merge(obj, *keys):
    return itertools.chain(*[obj[k] for k in keys])


def iter_until(func, pre=lambda x: False, post=lambda x: False):
    while 1:
        val = func()
        if pre(val):
            break
        yield val
        if post(val):
            break


class CachedProperty(object):

    def __init__(self, ttl=300):
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        try:
            value, last_update = inst._cache[self.__name__]
            if self.ttl > 0 and time.time() - last_update > self.ttl:
                raise AttributeError
        except (KeyError, AttributeError):
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}
            cache[self.__name__] = (value, time.time())
        return value


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


def humanize_bytes(b):
    abbrevs = (
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'B')
    )
    for factor, suffix in abbrevs:
        if b >= factor:
            break
    return '%.*f %s' % (2, b / float(factor), suffix)

def val_from_json(j, key, default=None):
    r = j
    try:
        for k in key.split('.'):
            if '[' in k and ']' in k:
                i = k.index('[')
                index = int(k[i + 1:-1])
                kn = k[:i]
                r = r[kn][index]
            else:
                r = r[k]
    except KeyError:
        return default
    except IndexError:
        return default
    except TypeError:
        return default

    return r

def has_val(j, key):
    return val_from_json(j, key) is not None

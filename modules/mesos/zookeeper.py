# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import contextlib

import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

from .. import log

TIMEOUT = 1

# Helper for testing
client_class = kazoo.client.KazooClient

@contextlib.contextmanager
def client(*args, **kwargs):
    zk = client_class(*args, **kwargs)
    try:
        zk.start(timeout=TIMEOUT)
    except kazoo.handlers.threading.TimeoutError:
        log.fatal(
            "Could not connect to zookeeper. " +
            "Change your config via `mesos config master`")
    try:
        yield zk
    finally:
        zk.stop()
        zk.close()

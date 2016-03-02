# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import logging
import contextlib

import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

import exceptions


logger = logging.getLogger('tutu.modules.mesos.' + __name__)
client_class = kazoo.client.KazooClient

@contextlib.contextmanager
def client(*args, **kwargs):
    zk = client_class(*args, **kwargs)
    try:
        zk.start(timeout=30)
    except kazoo.handlers.threading.KazooTimeoutError:
        logger.warn("Could not connect to zookeeper. ")
        raise exceptions.ZookeeperConnectionException()
    try:
        yield zk
    finally:
        zk.stop()
        zk.close()

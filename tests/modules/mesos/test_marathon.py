# -*- coding: utf-8 -*-

import unittest

from modules.mesos.marathon import MarathonResolver

class TestMarathonResolver(unittest.TestCase):
    def setUp(self):
        marathon_zk = 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster'
        self.resolver = MarathonResolver(marathon_zk)

    def tearDown(self):
        self.resolver = None

    def test_resolve_marathon_addresses(self):
        # This is actually like a integration test, you need a marathon cluster running 
        addresses = self.resolver.resolve()

        assert len(addresses) is 3

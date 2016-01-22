# -*- coding: utf-8 -*-

import unittest

from modules.mesos.master import MesosMaster

class TestMesosMaster(unittest.TestCase):
    def setUp(self):
        self.mesos_master = MesosMaster('http://localhost:5050')

    def tearDown(self):
        self.mesos_master = None

    def test_resolve_mesos_master(self):
        # This is actually like a integration test, you need a mesos master running in HA mode
        mesos_zk = "zk://localhost:2181/mesos"
        leader = self.mesos_master.resolve(mesos_zk)

        assert leader == '127.0.0.1:5050'

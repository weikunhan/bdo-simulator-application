# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2022 Weikun Han
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================
""" Simulator utility library Test
Author:
Weikun Han <weikunhan@g.ucla.edu>
Reference:
"""

import logging
import time
import unittest
from datetime import datetime
from utils.simulator_util import simulate_bdo_succeeded_rate_v1
from utils.simulator_util import simulate_bdo_succeeded_rate_v2
from utils.logger_util import initial_log

class TestSimulator(unittest.TestCase):
    ''' Simulator utility library Test'''

    def setUp(self):
        ''' Setup Test'''

        self.logger = initial_log()
        self.logger.level = logging.DEBUG
        self.succeeded_rate = 30.0
        self.time_range = 600
        self.time_buffer = 0
        self.simiulated_times = 10000
        self.time_utc_sec = int(datetime.utcnow().timestamp())

    def test_result_same(self):
        ''' Test regrasion error exist'''

        time_start = time.time()
        best_time_utc_sec_v1, best_succeeded_rate_v1 = simulate_bdo_succeeded_rate_v1(
            self.succeeded_rate,
            time_utc_sec=self.time_utc_sec,
            time_range=self.time_range,
            time_buffer=self.time_buffer,
            simiulated_times=self.simiulated_times)
        time_end = time.time()
        self.logger.info('Version 1 time spend: %s', time_end - time_start)
        time_start = time.time()
        best_time_utc_sec_v2, best_succeeded_rate_v2 = simulate_bdo_succeeded_rate_v2(
            self.succeeded_rate,
            time_utc_sec=self.time_utc_sec,
            time_range=self.time_range,
            time_buffer=self.time_buffer,
            simiulated_times=self.simiulated_times)
        time_end = time.time()
        self.logger.info('Version 2 time spend: %s', time_end - time_start)
        self.assertEqual(best_time_utc_sec_v1, best_time_utc_sec_v2)
        self.assertEqual(best_succeeded_rate_v1, best_succeeded_rate_v2)

if __name__ == '__main__':
    unittest.main()

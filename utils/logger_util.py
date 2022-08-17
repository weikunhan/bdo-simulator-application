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
""" Logger utility library
Author:
Weikun Han <weikunhan@g.ucla.edu>
Reference:
"""

import logging
import time
import os
from typing import Any

LOG_PATCH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

def get_time() -> str:
    """Get current system time"""

    return time.strftime('%Y%m%d_%H%M%S', time.localtime())

# pylint: disable=line-too-long
def initial_log(log_filepath: str = None) -> Any:
    """Initial log with the standard template"""

    if log_filepath is None:
        if not os.path.exists(LOG_PATCH):
            os.makedirs(LOG_PATCH)

        log_filepath =  os.path.join(LOG_PATCH, f'{get_time()}.log')

    logger = logging.getLogger()
    logger_format = logging.Formatter('[%(asctime)s]-[%(processName)s]-[%(threadName)s]-[%(levelname)s]: %(message)s')
    stream_handler = logging.StreamHandler()
    file_handdler = logging.FileHandler(log_filepath)
    stream_handler.setFormatter(logger_format)
    file_handdler.setFormatter(logger_format)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handdler)
    logger.setLevel(logging.INFO)

    return logger

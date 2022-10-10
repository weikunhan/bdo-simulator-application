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
""" Simulator utility library
Author:
Weikun Han <weikunhan@g.ucla.edu>
Li Qin <qinkroulis@gmail.com>
Reference:
"""


import logging
import multiprocessing as mp
from datetime import datetime
import numpy as np

logger = logging.getLogger()

def simulate_bdo_succeeded_rate_v1(
    succeeded_rate: float,
    simiulated_times = 10000,
    time_range: int = 600,
    time_buffer: int = 0,
    time_utc_sec: int = None
) -> tuple:
    """Predict game random generator bias for UTC time and succeeded rate

    Game used C++ implemetation.
    https://cplusplus.com/reference/cstdlib/rand/
    rand() is possible funntion to call, but is sometimes rather poor quality.

    https://en.cppreference.com/w/cpp/numeric/random
    Mersenne twister algorithm is better for random number generator

    https://stackoverflow.com/questions/9523570/random-number-generation-with-c-or-python
    The range for python set to [0, RAND_MAX].
    RAND_MAX is 32767 = 2^15-1, so the maximum value of a 16-bit signed integer.

    Args:
        succeeded_rate: the succeeded rate that user input
        simiulated_times: the total simulation run each second
        time_utc_in_sec: the current UTC time in seconds
        time_range: the future time window in seconds
        time_buffer: the possible server latch in seconds

    Returns:
        best_time_utc_sec
        best_succeeded_rate
    """

    best_time_utc_sec = 0
    best_succeeded_count = 0
    time_utc_now_sec = int(datetime.utcnow().timestamp())

    if time_utc_sec is not None:
        time_utc_now_sec = time_utc_sec

    logger.debug('succeeded_rate=%s, time_utc_now_sec=%s, time_range=%s, '
                 'time_buffer=%s, simiulated_times=%s. ',
                 succeeded_rate,
                 time_utc_now_sec,
                 time_range,
                 time_buffer,
                 simiulated_times)

    for i in range(time_range):
        positive_case_count = 0
        negative_case_count = 0
        random_seed_value = time_utc_now_sec + i
        np.random.seed(random_seed_value)

        for random_number in np.random.randint(32767, size=simiulated_times):
            current_rate = random_number % 10000

            # succeeded if random value is less or equal to the succeeded rate
            if current_rate <= succeeded_rate * 100:
                positive_case_count += 1

            # succeeded if random value is greater or equal to the failed rate
            if current_rate >= 10000 - succeeded_rate * 100:
                negative_case_count += 1

        logger.debug('time=%s, positive_case_count=%s, negative_case_count=%s. ',
                     random_seed_value,
                     positive_case_count,
                     negative_case_count)
        avg_succeeded_count = (positive_case_count + negative_case_count) / 2.0

        if avg_succeeded_count > best_succeeded_count:
            best_succeeded_count = avg_succeeded_count
            best_time_utc_sec = random_seed_value - time_buffer

    best_succeeded_rate = best_succeeded_count / float(simiulated_times) * 100
    return best_time_utc_sec, best_succeeded_rate


def simulate_bdo_succeeded_rate_v2(
    succeeded_rate: float,
    simiulated_times = 10000,
    time_range: int = 600,
    time_buffer: int = 0,
    time_utc_sec: int = None
) -> tuple:
    """Predict game random generator bias for UTC time and succeeded rate

    Game used C++ implemetation.
    https://cplusplus.com/reference/cstdlib/rand/
    rand() is possible funntion to call, but is sometimes rather poor quality.

    https://en.cppreference.com/w/cpp/numeric/random
    Mersenne twister algorithm is better for random number generator

    https://stackoverflow.com/questions/9523570/random-number-generation-with-c-or-python
    The range for python set to [0, RAND_MAX].
    RAND_MAX is 32767 = 2^15-1, so the maximum value of a 16-bit signed integer.

    This version is concurrent verison XCPU_COUNT faster than v1

    Args:
        succeeded_rate: the succeeded rate that user input
        simiulated_times: the total simulation run each second
        time_utc_in_sec: the current UTC time in seconds
        time_range: the future time window in seconds
        time_buffer: the possible server latch in seconds

    Returns:
        best_time_utc_sec
        best_succeeded_rate
    """

    best_time_utc_sec = 0
    best_succeeded_count = 0
    time_utc_now_sec = int(datetime.utcnow().timestamp())
    succeeded_rate *= 100

    if time_utc_sec is not None:
        time_utc_now_sec = time_utc_sec

    logger.debug('succeeded_rate=%s, time_utc_now_sec=%s, time_range=%s, '
                 'time_buffer=%s, simiulated_times=%s. ',
                 succeeded_rate,
                 time_utc_now_sec,
                 time_range,
                 time_buffer,
                 simiulated_times)
    pool = mp.Pool()
    args_list = [(succeeded_rate, simiulated_times, time_utc_now_sec + i)
                  for i in range(time_range)]
    res_list = pool.starmap_async(get_avg_succeeded_count, args_list).get()
    pool.close()
    pool.join()

    for i, res in enumerate(res_list):
        avg_succeeded_count = res

        if avg_succeeded_count > best_succeeded_count:
            best_succeeded_count = avg_succeeded_count
            best_time_utc_sec = time_utc_now_sec + i - time_buffer

    best_succeeded_rate = best_succeeded_count / float(simiulated_times) * 100
    return best_time_utc_sec, best_succeeded_rate

def get_avg_succeeded_count(
    succeeded_rate: float,
    simiulated_times: int,
    time_utc_in_sec: int
) -> float:
    """Get avarage succeeded count

    Args:
        simiulated_times: the total simulation run each second
        time_utc_in_sec: the UTC time in seconds

    Returns:
        avg_succeeded_count
    """

    positive_case_count = 0
    negative_case_count = 0
    np.random.seed(time_utc_in_sec)

    for random_number in np.random.randint(32767, size=simiulated_times):
        current_rate =  random_number % 10000

        # succeeded if random value is less or equal to the succeeded rate
        if current_rate <= succeeded_rate:
            positive_case_count += 1

        # succeeded if random value is greater or equal to the failed rate
        if current_rate >= 10000 - succeeded_rate:
            negative_case_count += 1

    logger.debug('time=%s, positive_case_count=%s, negative_case_count=%s. ',
                 time_utc_in_sec,
                 positive_case_count,
                 negative_case_count)
    return (positive_case_count + negative_case_count) / 2.0

def simulate_bdo_failed_rate_v1(
    succeeded_rate: float,
    simiulated_times = 10000,
    time_range: int = 600,
    time_buffer: int = 0,
    time_utc_sec: int = None
) -> tuple:
    """Predict game random generator bias for UTC time and succeeded rate

    Game used C++ implemetation.
    https://cplusplus.com/reference/cstdlib/rand/
    rand() is possible funntion to call, but is sometimes rather poor quality.

    https://en.cppreference.com/w/cpp/numeric/random
    Mersenne twister algorithm is better for random number generator

    https://stackoverflow.com/questions/9523570/random-number-generation-with-c-or-python
    The range for python set to [0, RAND_MAX].
    RAND_MAX is 32767 = 2^15-1, so the maximum value of a 16-bit signed integer.

    This version is concurrent verison XCPU_COUNT

    Args:
        succeeded_rate: the succeeded rate that user input
        simiulated_times: the total simulation run each second
        time_utc_in_sec: the current UTC time in seconds
        time_range: the future time window in seconds
        time_buffer: the possible server latch in seconds

    Returns:
        best_time_utc_sec
        best_failed_rate
    """

    best_time_utc_sec = 0
    best_failed_count = 0
    time_utc_now_sec = int(datetime.utcnow().timestamp())
    succeeded_rate *= 100

    if time_utc_sec is not None:
        time_utc_now_sec = time_utc_sec

    logger.debug('succeeded_rate=%s, time_utc_now_sec=%s, time_range=%s, '
                 'time_buffer=%s, simiulated_times=%s. ',
                 succeeded_rate,
                 time_utc_now_sec,
                 time_range,
                 time_buffer,
                 simiulated_times)
    pool = mp.Pool()
    args_list = [(succeeded_rate, simiulated_times, time_utc_now_sec + i)
                  for i in range(time_range)]
    res_list = pool.starmap_async(get_avg_failed_count, args_list).get()
    pool.close()
    pool.join()

    for i, res in enumerate(res_list):
        avg_failed_count = res

        if avg_failed_count > best_failed_count:
            best_failed_count = avg_failed_count
            best_time_utc_sec = time_utc_now_sec + i - time_buffer

    best_failed_rate = best_failed_count / float(simiulated_times) * 100
    return best_time_utc_sec, best_failed_rate

def get_avg_failed_count(
    succeeded_rate: float,
    simiulated_times: int,
    time_utc_in_sec: int
) -> float:
    """Get avarage falied count

    Args:
        simiulated_times: the total simulation run each second
        time_utc_in_sec: the UTC time in seconds

    Returns:
        avg_failed_count
    """

    positive_case_count = 0
    negative_case_count = 0
    np.random.seed(time_utc_in_sec)

    for random_number in np.random.randint(32767, size=simiulated_times):
        current_rate =  random_number % 10000

        # succeeded if random value is less or equal to the succeeded rate
        if current_rate > succeeded_rate:
            positive_case_count += 1

        # succeeded if random value is greater or equal to the failed rate
        if current_rate < 10000 - succeeded_rate:
            negative_case_count += 1

    logger.debug('time=%s, positive_case_count=%s, negative_case_count=%s. ',
                 time_utc_in_sec,
                 positive_case_count,
                 negative_case_count)
    return (positive_case_count + negative_case_count) / 2.0

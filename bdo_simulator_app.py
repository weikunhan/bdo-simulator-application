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
""" The Black Desert Online simulator web application
Author: 
Weikun Han <weikunhan@g.ucla.edu>
Li Qin <qinkroulis@gmail.com>
Reference:
"""

import time
from datetime import datetime
import numpy as np
import streamlit as st
import streamlit.components.v1 as stc

CUSTOM_TITLE = '''
<div style="font-size:40px;font-weight:bolder;background-color:#fff;padding:10px;
border-radius:10px;border:5px solid #464e5f;text-align:center;">
		<span style='color:black'>B</span>
		<span style='color:blue'>l</span>
		<span style='color:green'>a</span>
		<span style='color:red'>c</span>
		<span style='color:Orange'>k</span>
		<span style='color:black'>D</span>
		<span style='color:blue'>e</span>
		<span style='color:green'>s</span>
		<span style='color:red'>e</span>
		<span style='color:Orange'>r</span>
		<span style='color:grey'>t</span>
		<span style='color:black'>O</span>
		<span style='color:blue'>n</span>
		<span style='color:green'>l</span>
		<span style='color:red'>i</span>
		<span style='color:Orange'>n</span>
		<span style='color:grey'>e</span>		
</div>
'''

# pylint: disable=invalid-name
def simulate_bdo_succeeded_rate(
    succeeded_rate: float,
    simiulated_times = 10000,
    time_range: int = 600,
    time_buffer: int = 0,
    time_utc_sec: int = None
) -> tuple:
    '''Predict game random generator bias for UTC time and succeeded rate

    Game used C++ implemetation.

    https://cplusplus.com/reference/cstdlib/rand/
    rand() is possible funntion to call, but is sometimes rather poor quality.

    https://en.cppreference.com/w/cpp/numeric/random
    Mersenne twister algorithm is better for random number generator

    https://stackoverflow.com/questions/9523570/random-number-generation-with-c-or-python
    The range for python set to [0, RAND_MAX].
    RAND_MAX is 32767 = 2^15-1, so the maximum value of a 16-bit signed integer.

    Args:
        succeeded_rate:
            xxx
        time_utc_in_sec:
            xxx
        time_range:
            xxx
        time_buffer:
            xxx

    Returns:
        xxx

    Raises:
        xxx
    '''

    best_time_utc_sec = 0
    best_succeeded_count = 0
    time_utc_now_sec = int(datetime.utcnow().timestamp())

    if time_utc_sec is not None:
        time_utc_now_sec = time_utc_sec

    #print(f'succeeded_rate={succeeded_rate}, time_utc_in_sec={time_utc_now_sec},'
    #      f' time_range={time_range}, time_buffer={time_buffer},'
    #      f' simiulated_times={simiulated_times}')

    for i in range(time_range):
        positive_case_count = 0
        negative_case_count = 0
        #max_value = 0
        #min_value = sys.maxsize
        random_seed_value = time_utc_now_sec + i
        np.random.seed(random_seed_value)

        for n in np.random.randint(32767, size=simiulated_times):
            random_value = n % 10000
            #max_value = max(max_value, random_value)
            #min_value = min(min_value, random_value)

            # succeeded if random value is less or equal to the succeeded rate
            if random_value <= succeeded_rate * 100:
                positive_case_count += 1

            # succeeded if random value is greater or equal to the failed rate
            if random_value >= 10000 - succeeded_rate * 100:
                negative_case_count += 1

        #print(f'time={random_seed_value}, positive_case_count={positive_case_count},'
        #      f'negative_case_count={negative_case_count}')
        avg_succeeded_count = (positive_case_count + negative_case_count) / 2.0

        if avg_succeeded_count > best_succeeded_count:
            best_succeeded_count = avg_succeeded_count
            best_time_utc_sec = random_seed_value - time_buffer

    best_succeeded_rate = best_succeeded_count / float(simiulated_times) * 100
    return best_time_utc_sec, best_succeeded_rate

def main():
    ''' Main funtion'''

    #st.title('Black Desert Online simulator ')
    stc.html(CUSTOM_TITLE)
    menu = ['Black Desert Online simulator v1',
            'Black Desert Online simulator v2',
            'Black Desert Online simulator v3',
            'About']
    choice = st.sidebar.selectbox('Menu',menu)

    if choice == 'Black Desert Online simulator v1':
        st.subheader('Black Desert Online simulator v1')
        succeeded_rate = st.number_input(
            label='Please input your current succeeded rate: ',
            min_value=0.00,
            max_value=100.00,
            format='%.2f')
        st.info(f'The input succeeded rate: {succeeded_rate}%', icon="ℹ️")
        st.text('The current config setting for simulator')
        st.text(' - simulated_times (total simulation run each second): 10000')
        st.text(' - time_range (future time window in seconds): 600')
        st.text(' - time_buffer (possible server latch in seconds): 0')
        st.text(' - time_utc_sec (current UTC time): '
                f'{datetime.utcnow().strftime("%A, %B %d, %Y %I:%M:%S")}')

        if succeeded_rate:
            best_time_utc_sec, best_succeeded_rate = simulate_bdo_succeeded_rate(
                succeeded_rate)
            best_time_count = best_time_utc_sec - int(datetime.utcnow().timestamp())
            best_time_converted = datetime.fromtimestamp(best_time_utc_sec)
            st.success(f'The simulate result show best succeeded rate: '
                       f'{best_succeeded_rate:.2f}%', icon="✅")
            st.success(f'The simulate result show best time in: '
                       f'{best_time_converted.strftime("%A, %B %d, %Y %I:%M:%S")}',
                       icon="⚠️")
            ph = st.empty()

            for s in range(best_time_count, 0, -1):
                ph.metric('Countdown', f'{s // 60:02d}:{s% 60:02d}')
                time.sleep(1)
    elif choice == 'Black Desert Online simulator v2':
        st.subheader('Black Desert Online simulator v2')
        st.info('This is info')
        st.text('This is text')
        st.write(f'This is {"write"}')
    elif choice == 'Black Desert Online simulator v3':
        st.subheader('Black Desert Online simulator v3')
        st.info('This is info')
        st.text('This is text')
        st.write(f'This is {"write"}')
    else:
        st.subheader('About')
        st.success('Built with Streamlit')

if __name__ == '__main__':
    main()

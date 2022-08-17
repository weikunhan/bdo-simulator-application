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
import datetime
import streamlit as st
import streamlit.components.v1 as stc
from utils.simulator_util import simulate_bdo_succeeded_rate_v1
from utils.simulator_util import simulate_bdo_succeeded_rate_v2
from utils.simulator_util import simulate_bdo_failed_rate_v1

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

def main():
    ''' Main funtion'''

    #st.title('Black Desert Online simulator ')
    stc.html(CUSTOM_TITLE)
    menu = ['Black Desert Online simulator 1',
            'Black Desert Online simulator 2',
            'Black Desert Online simulator 3',
            'Black Desert Online simulator 4',
            'About']
    choice = st.sidebar.selectbox('Menu',menu)

    if choice == 'Black Desert Online simulator 1':
        st.subheader('Black Desert Online simulator succeeded rate v1')
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
                f'{datetime.datetime.utcnow().strftime("%A, %B %d, %Y %I:%M:%S")}')

        if succeeded_rate:
            time_counter = st.empty()

            with st.spinner('Start simulating result...'):
                best_time_utc_sec, best_succeeded_rate = simulate_bdo_succeeded_rate_v1(
                    succeeded_rate)

            best_time_count = best_time_utc_sec - int(datetime.datetime.utcnow().timestamp())
            best_time_converted = datetime.datetime.fromtimestamp(best_time_utc_sec)
            st.success(f'The simulate result show best succeeded rate: '
                       f'{best_succeeded_rate:.2f}%', icon="✅")
            st.warning(f'The simulate result show best time in: '
                       f'{best_time_converted.strftime("%A, %B %d, %Y %I:%M:%S")}',
                       icon="⚠️")

            for time_sec in range(best_time_count, 0, -1):
                time_counter.metric(
                    'Countdown', f'{time_sec // 60:02d}:{time_sec% 60:02d}')
                time.sleep(1)
    elif choice == 'Black Desert Online simulator 2':
        st.subheader('Black Desert Online simulator succeeded rate v2')
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
                f'{datetime.datetime.utcnow().strftime("%A, %B %d, %Y %I:%M:%S")}')

        if succeeded_rate:
            time_counter = st.empty()

            with st.spinner('Start simulating result...'):
                best_time_utc_sec, best_succeeded_rate = simulate_bdo_succeeded_rate_v2(
                    succeeded_rate)

            best_time_count = best_time_utc_sec - int(datetime.datetime.utcnow().timestamp())
            best_time_converted = datetime.datetime.fromtimestamp(best_time_utc_sec)
            st.success(f'The simulate result show best succeeded rate: '
                       f'{best_succeeded_rate:.2f}%', icon="✅")
            st.warning(f'The simulate result show best time in: '
                       f'{best_time_converted.strftime("%A, %B %d, %Y %I:%M:%S")}',
                       icon="⚠️")

            for time_sec in range(best_time_count, 0, -1):
                time_counter.metric(
                    'Countdown', f'{time_sec // 60:02d}:{time_sec% 60:02d}')
                time.sleep(1)
    elif choice == 'Black Desert Online simulator 3':
        st.subheader('Black Desert Online simulator failed rate v1')
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
                f'{datetime.datetime.utcnow().strftime("%A, %B %d, %Y %I:%M:%S")}')

        if succeeded_rate:
            time_counter = st.empty()

            with st.spinner('Start simulating result...'):
                best_time_utc_sec, best_failed_rate = simulate_bdo_failed_rate_v1(
                    succeeded_rate)

            best_time_count = best_time_utc_sec - int(datetime.datetime.utcnow().timestamp())
            best_time_converted = datetime.datetime.fromtimestamp(best_time_utc_sec)
            st.error(f'The simulate result show best failed rate: '
                     f'{best_failed_rate:.2f}%', icon="🚨")
            st.warning(f'The simulate result show best time in: '
                       f'{best_time_converted.strftime("%A, %B %d, %Y %I:%M:%S")}',
                       icon="⚠️")

            for time_sec in range(best_time_count, 0, -1):
                time_counter.metric(
                    'Countdown', f'{time_sec // 60:02d}:{time_sec% 60:02d}')
                time.sleep(1)
    elif choice == 'Black Desert Online simulator 4':
        st.subheader('Black Desert Online simulator failed rate v2')
        st.info('This is info')
        st.text('This is text')
        st.write(f'This is {"write"}')
    else:
        st.subheader('About')
        st.balloons()
        st.snow()

if __name__ == '__main__':
    main()

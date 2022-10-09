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
""" The Black Desert Online simulator web application on internet
Author:
Weikun Han <weikunhan@g.ucla.edu>
Reference:
"""

import os
import json
from pyngrok import ngrok

CONFIG_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'config', 'ngrok_config.json')

def main():
    """ Main funtion"""

    config_dict = json.loads(open(CONFIG_PATH, 'r', encoding='utf8').read())
    ngrok.set_auth_token(config_dict['authtoken'])
    internet_url = ngrok.connect(8501, bind_tls=True)
    ngrok_process = ngrok.get_ngrok_process()
    print('\n  You can now view your Streamlit app on internat in your browser.')
    print(f'\n  {internet_url}\n')

    try:
        # block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print("\n  You shutting down Streamlit app on the internet.\n")
        ngrok.kill()

if __name__ == '__main__':
    main()

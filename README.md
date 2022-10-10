# BDO Simulator Application
## Requirement
* Python 3.8 or above
* streamlit 1.12.0 or above
* numpy 1.23.1 or above
* (optional) pyngrok 5.1.0 or above
## Release Notes
* 2022/8/12 BDO Simulator succeeded rate case version 1 released
* 2022/8/16 BDO Simulator succeeded rate case version 2 released
* 2022/8/16 BDO Simulator failed rate case version 1 released
* 2022/10/5 BDO Simulater can run on the internet as well as localhost server
## Installation
Download repository
```
$ cd ~/
$ git clone https://github.com/weikunhan/bdo-simulator-application.git
```
Create [Python virtual environment](https://docs.python.org/3/library/venv.html)
```
$ python3 -m venv ~/bdo-simulator-application/venv
```
Active Python virual environment
```
$ source ~/bdo-simulator-application/venv/bin/activate
```
Install base Python packages
```
$ pip install streamlit
$ pip install numpy
```
(Optional) If you publish BDO Simulator (put localhost server on the internet), you need to install additional Python packages
```
$ pip install pyngrok
```
(Optional) Now that the ngrok agent is installed, let's connect it to your ngrok Account. If you haven't already, [sign up (or log in)](https://dashboard.ngrok.com/login) to the ngrok Dashboard and get your Authtoken. The ngrok agent uses the authtoken (sometimes called tunnel credential) to log into your account when you start a tunnel.
```
$ mkdir  ~/bdo-simulator-application/config
$ cat <<'EOF' > ~/bdo-simulator-application/config/ngrok_config.json
{
    "authtoken": "${your_token}"
}
EOF
$
```
*your_token - ngrok personal Authtoken, for example, aaaawvm1S7DhJeFSqyhmrGszLfR_72NcMpKWQ28YY8Xmsaaaa*
## Getting Started
Run BDO Simulator with [Streamlit](https://streamlit.io/) on localhost server
```
$ streamlit run bdo_simulator_app.py

  You can now view your Streamlit app in your browser.

  Network URL: http://172.18.220.15:8501
  External URL: http://73.193.118.28:8501

```
(Optional) Run BDO Simulator with Streamlit on the internet by [ngrok](https://ngrok.com/)
```
$ python run_bdo_simulator_app_internet.py

  You can now view your Streamlit app on internat in your browser.

  NgrokTunnel: "https://e9c8-73-193-118-28.ngrok.io" -> "http://localhost:8501"                   

```
*Now, copy https://e9c8-73-193-118-28.ngrok.io into your web browser*

*Don't close the localhost server terminal when running ngrook*
## Testing and Development
Run unit testing after development
```
$ python -m unittest discover tests
```
(Optional) Install static code analyser Python packages
```
$ pip install pylint
```
*Suggest veriable naming roles*
*xxx_count - the numbers data type in Python, which is the integer number used for counting*
*xxx_list - the list data type in Python*
*xxx_tuple - the tuple data type in Python*
*xxx_dict - the dictionary data type in Python*
"xxx" - the single word without underscore means that is user defined or imported object"
"xxx_xxx" - the multiple words with underscore means that instanced object method or veriable, which required more meaningful naming"
"xxx_xxx" - the multiple words with underscore also means that number data type or sting data type in Python, which required more meaningful naming"

## Screenshots
![](docs/example1.PNG)
![](docs/example2.PNG)
## License
[MIT License](LICENSE)
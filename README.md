# Sn00pXss

## Status
Started in July 2024.
In dev, comming soon... (soon = maybe one day).

## Description
This project aims to find XSS vulnerabilities. It uses `selenium` to interact with a chrome driver, and thus obtain all the data and detect whether an alert can be triggered with certain payloads. 

A request bin is also embeded in this project, which is very useful to steal cookies for example. To be sure that this tool works at all, I've tested it on multiple Root-me challenges that I have solved before.

Each vulnerability detection builds a configuration file in `Sn00pXss/saved_configs/` which represents the web page under test. It contains all the data needed by this script to inject payloads (submit buttons, vector identifier etc...). So, if you manually enter the configuration of a web page in the MANUAL attack mode, it will be saved and can be reused. It is automatically detected: if you launch the script with the same parameters (url, affected url) as before, the file name = hash(url + affected url).yaml is the same.


## Usage
First, install required python packages:
```bash
pip install -r requirements.txt
```

Then you can create `.env` file and fill the information (see `.env-example`).

For example:
```txt
CHROME_DRIVER_PATH=/path/to/chromedriver-linux64/chromedriver
CHROME_BINARY_PATH=/path/to/chrome-linux64/chrome
```

You can find both driver and binary here:
https://googlechromelabs.github.io/chrome-for-testing/

Then, wait for me to finish this project :)

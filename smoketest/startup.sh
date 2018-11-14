#!/usr/bin/env bash
node smoketest/createrunnumber.js &
python -m SimpleHTTPServer 8000&
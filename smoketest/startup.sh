#!/usr/bin/env bash
EXE=`which $0`
cd `dirname ${EXE}`
cd ..

kill `cat create.pid`
node smoketest/createrunnumber.js &
echo $! > create.pid
kill `cat http.pid`
python -m SimpleHTTPServer 8000&
echo $! > http.pid
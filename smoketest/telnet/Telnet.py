import telnetlib
import time, tempfile
import os, sys, re
import socket
import string


class TimeoutException(Exception):
    pass


class TelnetClient():
    ## @brief Telnet client initialisation
    def __init__(self, user="", password="", ip="", port=23, prompt="#", timeout=20, debug=False):
        self.DEBUG = debug
        #self.DEBUG = True
        self.client = None
        self.user = user
        self.password = password
        self.ip = ip
        self.prompt = prompt
        self.port = port
        self.lastDebug = ""
        if user and password and ip:
            if self.DEBUG: print ("Timeout: {0}".format(timeout))
            self.connect(user, password, ip, port, prompt, timeout)

    ## @brief Telnet client clean-up
    def __del__(self):
        if self.client:
            self.close()

    ## @brief internal debug message function
    # @param message the debug message to display
    def _debug(self, message):
        if self.DEBUG and message != self.lastDebug:
            print (message)
            self.lastDebug = message

    def _connect(self):
        if self.client:
            return
        con = telnetlib.Telnet()
        con.open(self.ip, self.port)
        # con.write("\n")
        con.read_until("login: ", 300)
        con.write(self.user + "\n")
        if self.password:
            result = con.read_until("Password: ", 5)
            if "Password" in result:
                con.write(self.password + "\n")
            else:
                con.write("\n")
                print ("\n\n@@@@@@ WARNING: No password prompt found. Board's password has been reset!! ({0}) @@@@@@\n\n".format(self.ip))
            #    raise IOError, "No password prompt. This is probably bad"

        self.client = con

    ## @brief checks Telnet connection, opens session if necessary
    def _checkconnection(self, retries=4):
        try:
            self.client.sock.sendall('\n')
            self._expect('#')
            # assert len(self.client.sock.recv(1024)) > 1
        except:
            if retries:
                self.close()
                try:
                    self._connect()
                    self._expect('#')
                except Exception as e:
                    print (str(e))
                self._checkconnection(retries-1)
            else:
                raise Exception('Failed to check connection for {0}'.format(self.ip))

    def _clean(self, recv):
        # invalid XML chars are removed
        invalid_xml = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', flags = re.MULTILINE)
        #remove unwanted \x1b[J escape sequences from output.
        recv = string.replace(recv, '[J', '')
        #recv = string.replace(recv, '\r\r', '')
        recv = string.replace(recv, '\r', '') # just in case of odd number of '\r's
        # remove invalid XML
        recv = invalid_xml.sub("", recv)
        return recv

    ## @brief searches Telnet response for a keyword
    # @param expect a keyword to search for (case sensitive)
    # @param wait the time to wait for a matching response
    # [default = 3]
    # @returns a list of response lines if the expected keyword is found
    def _expect(self, expect, wait=5, exact=False):
        self._debug("Telnet waiting for response '%s'" % expect)
        start = time.time()
        recv = ""
        response = []
        output = ""
        while time.time() - start < wait:
            while self.client.sock_avail() and time.time() - start < wait:
                recv += self.client.sock.recv(1024)
            recv = self._clean(recv)

            self._debug('received: "'+recv+'"')
            recv = re.sub(r'[^\n\x20-\x7e]', '', recv)
            lines = recv.splitlines()




            if len(lines):
                # remove empty string if first line
                if len(response) == 0 and len(lines[0]) == 0:
                    response += lines[1:] # skip first line
                else:
                    response += lines

                for line in lines:
                    output += line
                    if '--More--' in line:
                        return response
                    if expect in line:
                        return response
                    if not exact and expect in line:
                        return response
                if recv.endswith("\n"):
                    recv = ""
                else:
                    recv = response.pop()
            time.sleep (0.0001)
        if expect in output.replace('\n', ''):
            return response
        if recv: response.append(recv)
        print ("-----\nExpecting '{0}'. Received data was:".format(expect))
        for line in response: print (line)
        print ("-----")
        raise TimeoutException, "Telnet timeout waiting for expected response"

    ## @brief opens an Telnet connection and pseudo terminal
    # @param user the username for Telnet login
    # @param password the password for Telnet login
    # @param ip the ip address of the terminal to connect to
    # @param port the port to use for the connection
    # [default = 22]
    # @param prompt the shell prompt to expect
    # [default = "#"]
    # @param timeout the amount of time to try and connect
    # [default = 20]
    def connect(self, user, password, ip, port=23, prompt="#", timeout=360):
        self.close()
        self._debug("Telnet %s:%s@%s:%d" % (user, password, ip, port))
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.prompt = prompt
        start = time.time()
        while time.time() - start < timeout:
            try:
                self._checkconnection()
            except Exception as e:
                print ("Telnet connection error:", e)
            if self.client:
                print ("Telnet connection established to {0}".format(ip))
                return
            time.sleep(30)
        raise TimeoutException, "Telnet timeout trying to connect"


    ## @brief sends a command via Telnet
    # @param command the command to send via Telnet
    # @param expect the text to expect in the response
    # [default = prompt specified for connect()]
    # @param wait time to wait for send and response to complete
    # [default = 5]
    # @returns a list of response lines if the expected keyword is found
    # else returns None
    def send(self, command, expect=None, wait=30):
        self._checkconnection()
        self._debug("Telnet send command '%s'" % command.rstrip('\n'))
        start = time.time()
        #clear buffer
        while self.client.sock_avail() and time.time() - start < 2:
            self.client.sock.recv(1024)
        if expect is None:
            expect = self.prompt

        if not command.endswith('\n'):
            command += '\n'

        completeout = []
        repeat = True
        socketTimeout = False

        self._checkconnection() # replacing the one in the while

        while repeat:
            # self._checkconnection() # cannot check connection in the middle of doing something
            try:
                self.client.write(command)
                time.sleep(0.1) #give time for command/response
            except socket.error:
                if socketTimeout:
                    raise
                socketTimeout = True
                continue
            if expect is None:
                expect = self.prompt
            if expect:
                partial = self._expect(expect, time.time() + (wait - start))
                #if command == ' ':
                #    partial = partial[2:] # remove first two lines after sending space (more)
                #if partial [-1].startswith('--More--'):
                if '--More--' in partial[-1]:
                    completeout = completeout + partial[0:-1] #[0:-1] removes line with --More--
                    #add partial to complete (remove line with more)
                    # make sure another itereation of the loop is initiated with command ' '
                    command = ' '
                else:
                    #add partial to complete
                    completeout = completeout + partial
                    repeat = False

                    # to make output identical to ssh
#                    count = 0
#                    for item in completeout:
#                        if self.prompt in item:
#                            break
#                        count += 1
#                    for i in range(count):
#                        output.pop(0)
#                    output[0] = command.strip('\n')

                    return completeout
        return None

    ## @brief Same as send, but forcing exact output matching
    ## @brief Only line starting with prompt is matched
    ## @brief prompt in the middle of the line will be ignored
    # @param command the command to send via Telnet
    # @param expect the text to expect in the response
    # [default = prompt specified for connect()]
    # @param wait time to wait for send and response to complete
    # [default = 5]
    # @returns a list of response lines if the expected keyword is found
    # else returns None
    def sendTrue(self, command, expect=None, wait=5):
        self._checkconnection()
        self._debug("Telnet send command '%s'" % command.rstrip('\n'))
        start = time.time()
        #clear buffer
        while self.client.sock_avail():
            self.client.sock.recv(1024)
        if expect is None:
            expect = self.prompt
        else:
            self.prompt = expect

        if not command.endswith('\n'):
            command += '\n'

        completeout = []
        repeat = True
        socketTimeout = False

        while repeat:
            try:
                self.client.write(command)
                time.sleep(0.2) #give time for command/response
            except socket.error:
                if socketTimeout:
                    raise
                socketTimeout = True
                continue
            if expect is None:
                expect = self.prompt
            if expect:
                partial = self._expect(expect, time.time() + (wait - start), True)
                if command == ' ':
                    partial = partial[2:] # remove first two lines after sending space (more)
                #if partial [-1].startswith('--More--'):
                if '--More--' in partial[-1]:
                    completeout = completeout + partial[0:-3] #[0:-1] removes line with --More--
                    #add partial to complete (remove line with more)
                    # make sure another itereation of the loop is initiated with command ' '
                    command = ' '
                else:
                    #add partial to complete
                    completeout = completeout + partial
                    repeat = False
                    return completeout
        return None

    ## @brief sends a command Ctrl-C via Telnet
    # @param command the command to send via Telnet
    # @param expect the text to expect in the response
    # @param wait time to wait for send and response to complete
    def sendControl(self, command, expect=None, wait=5):
        self._debug('Telnet send control-C')
        self.client.write('\x03')
        if expect is None:
            expect = self.prompt
        self.client.expect(expect, timeout=wait)

    ## @brief closes current Telnet connection
    def close(self):
        if self.client:
            try:
                self.client.write('end\n')
                self.client.write('exit\n')
            except:
                pass
            time.sleep(2)
            self.client.close()
            self.client = None


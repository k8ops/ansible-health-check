#!/usr/bin/env python
# coding=utf-8
# Author: Sean Ly <seanly@aliyun.com>

from ansible.module_utils.basic import *
import time
import socket
import re
import sys


def check_server(address, port, timeout):
    # Create a TCP socket
    s = socket.socket()
    print "Attempting to connect to %s on port %s" % (address, port)
    s.settimeout(timeout)
    try:
        s.connect((address, port))
        print "Connected to %s on port %s" % (address, port)
        return True
    except socket.error, e:
        print "Connection to %s on port %s failed: %s" % (address, port, e)
        return False


def main():
    module = AnsibleModule(
        argument_spec = dict(
            address = dict(required=True),
            port = dict(request=True, type="int"),
            initial_delay = dict(required=False, type='int', default=0),
            delay_between_tries = dict(required=False, type='int', default=5),
            max_retries = dict(required=False, type='int', default=10),
            timeout = dict(request=False, type='int', default=10),
        )
    )

    address = module.params['address']
    port = module.params['port']
    initial_delay = module.params['initial_delay']
    delay_between_tries = module.params['delay_between_tries']
    max_retries = module.params['max_retries']
    timeout = module.params['timeout']

    time.sleep(initial_delay)
    info = ''
    for attempt in xrange(max_retries):
        if attempt != 0:
            time.sleep(delay_between_tries)
        success = check_server(address=address, port=port, timeout=timeout)
        if success:
            module.exit_json(failed_attempts=attempt)
    else:
        module.fail_json(msg='Maximum attempts reached: ' + info,
                         failed_attempts=attempt)

main()


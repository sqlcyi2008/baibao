import redis
import sys
import os
import signal
import getopt
from subprocess import Popen, PIPE, STDOUT
from chromote import Chromote
from time import sleep

def sig_handler(sig, frame):
    try:
        os.system("kill -9 `lsof -t -i:9222`")
        exit(0)
    except Exception, ex:
        exit(0)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    # set signal handler
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        # more code, unchanged
        # os.system("google-chrome")
        proc = Popen("google-chrome", shell=True, stdout=PIPE, stderr=STDOUT)
        sleep(1)
        chrome = Chromote()
        tab = chrome.tabs[0]
        tab.set_url('http://127.0.0.1:8080/examples/servlets/servlet/HelloWorldExample')
        while True:
            tab.reload()
            sleep(9)
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

import redis
import sys
import os
import signal
import getopt
from subprocess import Popen, PIPE, STDOUT


def sig_handler(sig, frame):
    try:
        # os.system("kill -9 `lsof -t -i:8080`")
        exit(0)
    except Exception, ex:
        exit(0)


def getbreakpoint(line):
    bpstr = str(line)
    bpstr = bpstr.replace('/', '.')
    start = bpstr.find('.src.')
    end = bpstr.find('.java:')
    # print str(start)+'##'
    # print str(end) + '##'
    # print bpstr[start+5:end]
    return bpstr[start + 5:end]+':'+bpstr.split(':')[1]

def getexpress(line):
    eprstr = str(line)
    strlen = len(eprstr)
    start = eprstr.find('//??')
    return eprstr[start+4:strlen]

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
        cmd = "find  /root/dushiniang/src -name \*.java -exec grep -n -H \"//??\" {} \;"
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print line.replace('\n', '')
            bpline = line.replace('\n', '')
            bplocation = getbreakpoint(bpline)
            bpepr = getexpress(bpline)

            # print(line, '')
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.sadd("breakpoints", bplocation)
            r.set(bplocation,bpepr)

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

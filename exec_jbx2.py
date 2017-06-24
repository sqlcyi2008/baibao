import redis
import sys
import os
import signal
import getopt
from subprocess import Popen, PIPE, STDOUT


def sig_handler(sig, frame):
    try:
        os.system("kill -9 `lsof -t -i:8080`")
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
        proc = Popen("cd ~/dushiniang/;java -jar ~/dushiniang/jbx.jar", shell=True, stdout=PIPE, stderr=STDOUT)
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            # print line.replace('\n', '')
            # print(line, '')
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.lpush("baibaoxiang", "exec_jbx=" + line.replace('\n', ''))

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

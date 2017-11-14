import subprocess
import time
import threading
from time import ctime,sleep

#jdb子进程
global proc

def outThread(var):

    while True:
        global proc
        line = proc.stdout.readline()
        if not line:
            break
        line =line.decode('gbk')
        print(line)
        if 'Server startup in' in line:
            msg = 'trace go methods\r\n'.encode('utf-8')
            proc.stdin.write(msg)
            proc.stdin.flush()


def main():
    outthr = threading.Thread(target=outThread, args=(u'线程1',))

    command = 'jdb.exe -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'

    #return
    global proc
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # print process1.communicate()[0]

    line = proc.stdout.readline()
    print(line.decode('gbk'))
    line = proc.stdout.readline()
    print(line.decode('gbk'))
    line = proc.stdout.readline()
    print(line.decode('gbk'))
    line = proc.stdout.readline()
    print(line.decode('gbk'))
    line = proc.stdout.readline()
    print(line.decode('gbk'))

    msg = 'cont\r\n'.encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

    outthr.setDaemon(True)
    outthr.start()

    msg = 'exclude flex.*,com.microsoft.*,org.apache.*,java.*,sun.*,javax.*,org.loushang.*,com.sun.*,org.json.*,org.xml.*\r\n'.encode('utf-8')
    proc.stdin.write(msg)
    proc.stdin.flush()

    '''
    msg = 'trace go methods\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()
    '''
    outthr.join()

if __name__ == '__main__':
    main()

import subprocess
import time


def main():

    command = 'jdb.exe -launch -Djdk.tls.ephemeralDHKeySize=2048 -Djava.util.logging.config.file=D:\\apps\\apache-tomcat-7.0.72\\conf\\logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djava.endorsed.dirs=D:\\apps\\apache-tomcat-7.0.72\\endorsed -classpath D:\\apps\\apache-tomcat-7.0.72\\bin\\bootstrap.jar;D:\\apps\\apache-tomcat-7.0.72\\bin\\tomcat-juli.jar -Dcatalina.base=D:\\apps\\apache-tomcat-7.0.72 -Dcatalina.home=D:\\apps\\apache-tomcat-7.0.72 -Djava.io.tmpdir=D:\\apps\\apache-tomcat-7.0.72\\temp org.apache.catalina.startup.Bootstrap start'

    process1 = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    # print process1.communicate()[0]

    line = process1.stdout.readline()
    print(line.decode('gbk'))
    line = process1.stdout.readline()
    print(line.decode('gbk'))
    line = process1.stdout.readline()
    print(line.decode('gbk'))
    line = process1.stdout.readline()
    print(line.decode('gbk'))
    line = process1.stdout.readline()
    print(line.decode('gbk'))

    msg = 'cont\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()

    msg = 'exclude flex.*,com.microsoft.*,org.apache.*,java.*,sun.*,javax.*,org.loushang.*,com.sun.*,org.json.*,org.xml.*\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()

    '''
    msg = 'trace go methods\r\n'.encode('utf-8')
    process1.stdin.write(msg)
    process1.stdin.flush()
    '''

    while True:
        line = process1.stdout.readline()
        if not line:
            break
        print(line.decode('gbk'))



if __name__ == '__main__':
    main()

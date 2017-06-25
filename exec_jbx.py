import redis
import signal
import os
from subprocess import Popen, PIPE, STDOUT

proc = Popen("cd ~/dushiniang/;"
             "java -jar /root/dushiniang/jbx.jar -Djava.util.logging.config.file=/root/dushiniang/apache-tomcat-7.0"
             ".72/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager "
             "-Djdk.tls.ephemeralDHKeySize=2048 -Djava.endorsed.dirs=/root/dushiniang/apache-tomcat-7.0.72/endorsed "
             "-classpath /root/dushiniang/apache-tomcat-7.0.72/bin/bootstrap.jar:/root/dushiniang/apache-tomcat-7.0"
             ".72/bin/tomcat-juli.jar -Dcatalina.base=/root/dushiniang/apache-tomcat-7.0.72 "
             "-Dcatalina.home=/root/dushiniang/apache-tomcat-7.0.72 "
             "-Djava.io.tmpdir=/root/dushiniang/apache-tomcat-7.0.72/temp", shell=True, stdout=PIPE, stderr=STDOUT)


def sig_handler(sig, frame):
    try:
        os.system("kill -9 `lsof -t -i:8080`")
        exit(0)
    except Exception, ex:
        exit(0)


signal.signal(signal.SIGTERM, sig_handler)
# signal.signal(signal.SIGINT, sig_handler)


while True:
    line = proc.stdout.readline()
    if not line:
        break
    # print line.replace('\n', '')
    # print(line, '')
    #r = redis.Redis(host='localhost', port=6379, db=0)
    #r.lpush("baibaoxiang", "exec_jbx=" + line.replace('\n', ''))

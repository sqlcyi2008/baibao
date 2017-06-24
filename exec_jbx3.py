import pexpect

child = pexpect.spawn('/root/dushiniang/jbx.sh')
fout = open('/root/mylog.txt', "w")
child.logfile = fout
child.expect('>')
child.sendline('exclude org.*,java.*,sun.*,javax.*,com.*,flex.*,edu.*')

child.expect('>')
child.sendline('stop at HelloWorldExample:46')

child.expect('>')
child.sendline('run org.apache.catalina.startup.Bootstrap  start')

child.expect('.*Server startup in.*')
child.sendline('trace go methods')

child.expect('http-bio-8080-exec-1.*')
child.sendline('locals')

child.expect('http-bio-8080-exec-1.*')
child.sendline('cont')

child.expect('>')
child.sendline('cont')

child.expect(pexpect.EOF)
fout.close()

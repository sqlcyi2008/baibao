import commands
import redis

(status, output) = commands.getstatusoutput("find /media/sf_dev/workspace -name WEB-INF -type d")
print status
print output
if output:
    ls = output.splitlines()
    print ls
    for app_path in ls:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.lpush("baibaoxiang", "app_path="+app_path)

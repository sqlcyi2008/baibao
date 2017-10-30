import psutil
import json

for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name','cmdline'])
    except psutil.NoSuchProcess:
        pass
    else:
        if pinfo.get("cmdline"):
            jj = json.dumps(pinfo)
            print(jj)

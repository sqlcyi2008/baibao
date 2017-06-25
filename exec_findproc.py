import os
cmd = 'wmic process where caption="java.exe" get caption,commandline /value'

os.system(cmd)
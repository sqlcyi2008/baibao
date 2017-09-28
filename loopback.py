from winpcapy import WinPcapUtils

from winpcapy import WinPcapDevices
# Return a list of all the devices detected on the machine
WinPcapDevices.list_devices()

 # Itearte over devices (in memory), with full details access
with WinPcapDevices() as devices:
    for device in devices:
        print device.description

from ctypes import *
from numpy import *

addHeader_config_path="/home/dell-r200/lwh/ipv6_addHeader.so"
addHeader = CDLL(addHeader_config_path)

interfaceName = "eno1"
serverIP= "fe80::2e8:997e:73bf:c6ab"
port=80
option_type=0x3c
apn_value1 = 0x01020304
apn_value2 = 0x05060708
request_path = "/111.ts"
output_path = "test0710.ts"

print(type(option_type))
print(type(apn_value1))
print(type(serverIP))
print(type(request_path))

status = addHeader.add_HBH(interfaceName.encode(), serverIP.encode(), int(port), int(option_type), int(apn_value1), int(apn_value2), request_path.encode(), output_path.encode())
print("status code:",status)
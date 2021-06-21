import socket, netifaces

# Getting local ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADDRESS = s.getsockname()[0]

# Getting default gateway
gateways = netifaces.gateways()
DEFAULT_GATEWAY = gateways['default'][netifaces.AF_INET][0]

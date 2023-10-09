import socket

try:
    ip_address = socket.gethostbyname('s794.kdltps.com')
    print("IP address:", ip_address)
except socket.gaierror as e:
    print("Failed to resolve hostname:", e)
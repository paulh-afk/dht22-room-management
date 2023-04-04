import socket 

print("Welcome to the initialization program\n")

ip = socket.gethostbyname(socket.gethostname()) 
if ip == '127.0.0.0':
  print("Your device is not connected to the internet, check that it is connected to your network!\n")
else:
  print(f"Your device is connected to a private network and has the ip address {ip}!\n")

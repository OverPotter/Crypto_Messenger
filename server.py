import socket, time, re 

BUFFER_SIZE = 1024
host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []
logging = []

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))

st_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

quit = False
print("[ Server Started ] at " + st_time +"\n")

while not quit:
	try:
		data, addr = s.recvfrom(BUFFER_SIZE)

		if addr not in clients:
			clients.append(addr)
			alias = str(data)
			alias = alias[2:-1]
			alias = re.search(r"\[\w*\]",alias)
			alias = alias.group(0)
			logging.append(alias)
			logging.append(addr)   

		itsatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

		print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
		print(data.decode("utf-8"))

		for client in clients:
			if addr != client:
				s.sendto(data,client)
	except:
		print("\n[ Server Stopped ] at " + itsatime)
		quit = True

with open("logging.txt", "w") as clients_list:
	logging = str(logging)
	logging = logging[:-1]
	logging = re.sub(r"',\s", ":", logging)
	logging = re.sub(r"['\[()]", "", logging).replace(", ", "\n")
	logging = re.sub(r"\]:", " => ", logging)
	clients_list.write(logging)

s.close()
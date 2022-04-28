import socket, threading, time, re, sys
import OAEP_lib

shutdown = False
join = False
BUFFER_SIZE = 1024

def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(BUFFER_SIZE)
				data = str(data)
				data = data[2:-1]
				if re.search(r"\[\w*\]\s\=>\s\bjoin to chat\b", data) or re.search(r"\[\w*\]\s\<=\s\bleft from chat\b", data):
					print(data)
				else:
					alias = re.sub(r'\d', '', data)
					data = re.sub(r'\D', '', data)
					data = OAEP_lib.OAEP_decr(int(data))
					OAEP_lib.integrity(int(data))
					print(alias + OAEP_lib.output(data))

				time.sleep(0.2)     
		except: pass

host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.100.7",9090)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

alias = input("Pleasure, use only letters and numbers\nName: ")
if bool(re.search(r'\W', alias)): sys.exit()

rT = threading.Thread(target = receving, args = ("RecvThread",s))
rT.start()

while shutdown == False:
	if join == False:
		s.sendto(("[" + alias + "] => join to chat").encode("utf-8"),server)
		join = True
	else:
		try:
			message = input()
			mess = str(OAEP_lib.OAEP_encr(message))

			if mess != "":
				s.sendto(("[" + alias + "] :: "+mess).encode("utf-8"),server)
			
			time.sleep(0.2)
		except:
			s.sendto(("[" + alias + "] <= left from chat").encode("utf-8"),server)
			shutdown = True

rT.join()
s.close()

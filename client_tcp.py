import socket
from pacote import *

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print('Para sair use CTRL+X\n')
msg = ('opa','tit',8,2, 941.9, object)
print(msg)
print(pack(msg))
data = pack(msg)
tcp.send(data.encode())
response = tcp.recv(1024).decode()
r = unpack(response)
print(r)
tcp.close()

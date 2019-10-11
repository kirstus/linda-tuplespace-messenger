import socket
from pacote import *
from random import randint

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

#tuple (author, topic, msg [, ad hoc ]* [, topic_index, author_in_topic_index])

while True:
    # load tuples from disk
    con, cliente = tcp.accept()
    print('Conectado por', cliente)
    while True:
        #msg received: (operation, [passwd,] tuple)
        data = con.recv(1024).decode()
        if not data: break
        msg = unpack(data)
        #if opening connection: validate user
        #   else: refuse and ask for (correct) passwd
        #parse operation
        #call operation
        #   store the changes on disk
        #send response
        response = ('OK',1)
        #msg sent: (status, [error_msg,] tuple)
        con.send(pack(response).encode())
        print(cliente, msg)
    print('Finalizando conexao do cliente', cliente)
    con.close()

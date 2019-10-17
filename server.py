import socket
from pacote import *
from random import randint
import lindatp
from flask import Flask, jsonify

class Servidor():
    def __init__(self):
        print('init serv')
        self.lnd = lindatp.lindatp()

    def init(self):
        HOST = ''              # Endereco IP do Servidor
        PORT = 5001            # Porta que o Servidor esta
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)
        self.tcp.bind(orig)
        self.tcp.listen(1)

    def parse(self, msg):
        operation = msg.pop(0)
        if operation == 'read':
            t = self.lnd.rdp(tuple(msg))
            return t
        passwd = msg.pop(0)
        if operation == 'write':
            t = self.lnd.outp(tuple(msg),passwd)
        elif operation == 'remove':
            t = self.lnd.inp(tuple(msg),passwd)
        print(operation, passwd)
        print(msg)
        return t

    def send_msg(self, t, passwd):
        return self.lnd.outp(t, passwd)

    def delete_msg(self, topic, msg_id, passwd):
        return self.lnd.delete_msg(topic, msg_id, passwd)
    
    def get_topics(self):
        return {'topics' : self.lnd.get_topics()}

    def get_authors(self):
        return {'authors' : self.lnd.get_authors()}

    def get_messages(self, topic):
        return {'messages': self.lnd.get_messages(topic)}

    def get_msg(self):
        #t = self.lnd.rdp(tuple(msg))
        t = ('aa','bb','cc','dd','ee')
        return to_json(t)

    # tuple = (autor, topico, msg, [ ... ,]* time_sent, msg_number)
    def listen(self):
        while True:
            # load tuples from disk
            con, cliente = self.tcp.accept()
            print('Conectado por', cliente)
            while True:
                #msg received: (operation, [passwd,] tuple)
                data = con.recv(1024).decode()
                if not data: break
                msg = unpack(data)
                self.parse(msg)
                #r = lnd.rdp(tuple(msg))
                #if opening connection: validate user
                #   else: refuse and ask for (correct) passwd
                #parse operation
                #call operation
                #   store the changes on disk
                #send response
                response = ('OK',1)
                #response = r
                #msg sent: (status, [error_msg,] tuple)
                con.send(pack(response).encode())
                print(cliente, msg)
            print('Finalizando conexao do cliente', cliente)
            con.close()

if __name__ == '__main__':
    s = Servidor()
    s.init()
    s.listen()

import socket
from pacote import *

class Cliente():
    
    def __init__(self):
        #self.set_username()
        #self.set_passwd()
        #self.set_topic()
        return    

    #def __new__(self):
    #    HOST = '127.0.0.1'     # Endereco IP do Servidor
    #    PORT = 5000            # Porta que o Servidor esta
    #    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    dest = (HOST, PORT)
    #    tcp.connect(dest)

    def __del__(self):
        self.tcp.close()

    def init(self):
        self.set_username()
        self.set_passwd()
        self.set_topic()
        HOST = '127.0.0.1'     # Endereco IP do Servidor
        PORT = 5001            # Porta que o Servidor esta
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (HOST, PORT)
        self.tcp.connect(dest)
        
    def set_passwd(self):
        self.passwd = str(input('Insira sua senha: '))
    
    def set_username(self):
        self.username = str(input('Insira seu nome: '))

    def set_topic(self):
        self.current_topic = str(input('Insira o tópico: '))

    def printa(self):
        print(self.set_passwd)
        print(self.set_username)
        print(self.set_topic)

    def writemsg(self):
        msg = str(input('escreva sua mensagem: '))
        while msg != '\x18':
            self.write(msg)
            msg = str(input('escreva sua mensagem: '))

    def write(self, msg):
        t = (self.passwd, self.username, self.current_topic, msg, 0, 0)
        self.send(t, 'write')

    def send(self, t, operation):
        data = pack(tuple([operation])+t)
        self.tcp.send(data.encode())
        response = self.tcp.recv(1024).decode()
        r = unpack(response)
        print(r)

    def readnext(self, topic, index):
        t = (object, topic, object, object, index)
        self.send(t, 'read')

    def delete(self, topic, msg = object, index = object):
        t = (self.passwd, self.username, topic, msg, object, index)
        self.send(t, 'delete')
        

if __name__ == '__main__':
    c = Cliente()
    c.init()
    print(c)
    msg = 'olar'
    print(msg)
    c.write(msg)
    c.writemsg()

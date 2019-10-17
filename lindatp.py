import hashlib, binascii, os, time
from pacote import *


# tuple = (autor, topico, msg, [ ... ,]* time_sent, msg_number)
class lindatp():
    tuplespace = {}

    def __init__(self):
        self.tuples = open('tuples.txt','r+')
        self.passwd = open('passwd.txt','r+')
        self.msgnum  = open('msgnum.txt','r+')
        self.import_tuples()
        self.tuples.close()
        self.passwd.close()
        self.msgnum.close()
        self.tuples = open('tuples.txt','w+')
        self.passwd = open('passwd.txt','w+')
        self.msgnum  = open('msgnum.txt','w+')
        #self.tuples.write('oi\n')
        #self.tuples.write('nice\n')

    def __del__(self):
        if self.tuplespace != {}:
            self.export_tuples()
        #self.tuples.write('tchau\n')
        self.tuples.close()
        self.passwd.close()
        self.msgnum.close()

    def delete_msg(self, topic, msg_id, passwd):
        t = (object, topic, object, object, msg_id)
        r = self.inp(t, passwd)
        return r

    def get_topics(self):
        #return {'topics': list(self.tuplespace[5].keys())}
        ts =self.tuplespace[5]['topic']
        return list(ts.keys())

    def get_authors(self):
        ts =self.tuplespace[5]['author']
        return list(ts.keys())

    def get_messages(self,topic):
        l = []
        ts =self.tuplespace[5]['topic'][topic]
        for author in ts:
            for t in ts[author]:
                d = {   'author': t[0],
                        'topic': t[1],
                        'msg':  t[2],
                        'timestamp': t[3],
                        'id':       t[4]
                    }
                l.append(d)
        return self.insertionSort(l,'timestamp')
        
    def insertionSort(self, inputArray, atr):
        n = len(inputArray)
        for i in range(1,n):
            key = inputArray[i][atr]
            tuplekey = inputArray[i]
            j = i-1
            while (j >= 0 and inputArray[j][atr]>key):
                inputArray[j+1] = inputArray[j]
                j = j - 1
            inputArray[j+1] = tuplekey
        return inputArray

    def export_tuples(self):
        for n in self.tuplespace:
            #print(n)
            tsn = self.tuplespace[n]
            for autor in tsn['author']:
               # print(autor, len(tsn['author'][autor]))
                for topico in tsn['author'][autor]:
                    if tsn['author'][autor][topico] != 0:
                        #print(topico, len(tsn['author'][autor][topico]))
                        for tupla in tsn['author'][autor][topico]:
                            #print(tupla)
                            #print(pack(tupla))
                            #print(unpack(pack(tupla)))
                            self.tuples.write(pack(tupla)+'\n')
            for author in tsn['passwd']:
                p = (author, tsn['passwd'][author], n)
                #print(pack(p))
                self.passwd.write(pack(p)+'\n')
            for topic in tsn['msg_numbers']:
                mn = (topic , tsn['msg_numbers'][topic], n)
                #print(mn)
                self.msgnum.write(pack(mn)+'\n')

    def import_tuples(self):
        for l in self.tuples.readlines():
            t = unpack(l)
            #print(tuple(t))
            self.insert(tuple(t))
        for l in self.passwd.readlines():
            t = unpack(l)
            #print(tuple(t))
            self.insertpasswd(tuple(t))
        for l in self.msgnum.readlines():
            t = unpack(l)
            #print(tuple(t))
            self.insertnumbers(tuple(t))

    def insert(self, t):
        if len(t) not in self.tuplespace:
            ts = {  'author': {},
                    'topic': {},
                    'passwd': {},
                    'msg_numbers': {}}
            self.tuplespace[len(t)] = ts

        indice = self.tuplespace[len(t)]
        author = t[0]
        topic = t[1]

        #author = hash(author)
        #topic = hash(topic)
        el = []
        if author not in indice['author']:
            td = {topic: el}
            indice['author'][author] = td
    
        if topic not in indice['topic']:
            ad = {author: el}
            indice['topic'][topic] = ad

        if author not in indice['topic'][topic]:
            indice['topic'][topic][author] = el

        if topic not in indice['author'][author]:
            indice['author'][author][topic] = el
    
        indice['author'][author][topic].append(t)

    def insertpasswd(self, t):
        indice = self.tuplespace[t[2]]
        author = t[0]
        if author not in indice['passwd'].keys():
            indice['passwd'][author] = t[1]


    def insertnumbers(self, t):
        topic = t[0]
        indice = self.tuplespace[t[2]]
        if topic not in indice['msg_numbers']:
            indice['msg_numbers'][topic] = t[1]
        indice['msg_numbers'][topic] = t[1]

    def hash_password(self,password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self,stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def check_empty(self, author, passwd, topic):
        if author is '':
            print('Nome do autor não pode ser em branco!')
            return False
        elif type(author) is not str:
            print('autor não pode ser um número!')
            return False
    
        if passwd is '':
            print('senha não pode ser em branco!')
        elif type(passwd) is not str:
            print('senha não pode ser um número!')
            return False
        
        if topic is '':
            print('Nome do tópico não pode ser em branco!')
            return False
        elif type(topic) is not str:
            print('topico não pode ser um número!')
            return False
    
    def outp(self,t, passwd):
        if len(t) not in self.tuplespace:
            ts = {  'author': {},
                    'topic': {},
                    'passwd': {},
                    'msg_numbers': {}}
            self.tuplespace[len(t)] = ts
    
        indice = self.tuplespace[len(t)]
        author = t[0]
        topic = t[1]
        
        if author is '':
            print('Nome do autor não pode ser em branco!')
            return False
        elif type(author) is not str:
            print('autor não pode ser um número!')
            return False
    
        if passwd is '':
            print('senha não pode ser em branco!')
        elif type(passwd) is not str:
            print('senha não pode ser um número!')
            return False
        
        if topic is '':
            print('Nome do tópico não pode ser em branco!')
            return False
        elif type(topic) is not str:
            print('topico não pode ser um número!')
            return False
    
        #author = hash(author)
        #topic = hash(topic)
        #print('hashes: ', author, topic)
        el = []
        if author not in indice['author']:
            td = {topic: el}
            indice['author'][author] = td
    
        if topic not in indice['topic']:
            ad = {author: el}
            indice['topic'][topic] = ad

        if topic not in indice['msg_numbers']:
            indice['msg_numbers'][topic] = 0

        if author not in indice['topic'][topic]:
            indice['topic'][topic][author] = el

        if topic not in indice['author'][author]:
            indice['author'][author][topic] = el
    
        if author not in indice['passwd'].keys():
            indice['passwd'][author] = self.hash_password(passwd)
        elif self.validate_user(t, passwd) == False:
            return False
        
        timenow = time.time()
        indice['msg_numbers'][topic] += 1
        indice['author'][author][topic].append(t[0:-2]+(timenow,indice['msg_numbers'][topic]))
        #print(indice['author'][author][topic])
        #indice['topic'][topic][author].append(t[0:-2]+(timenow,1))
        #print(indice['topic'][topic][author])
        #print(self.tuplespace[len(t)])
    
    def validate_args(self,t):
        if len(t) not in self.tuplespace:
            return False
        indice = self.tuplespace[len(t)]
        author = t[0]
        topic  = t[1]
    
        if type(author) is not str and type(author) is not type:
            print('autor não pode ser um número!')
            return False
        
        if type(author) is not str and type(author) is not type:
            print('topico não pode ser um número!')
            return False
    
        if type(author) is type and type(topic) is type:
            print('deve ser fornecido ao menos um dos parâmetros posicionais de identificação (autor|tópico)')
            return False
    
        h_author = author
        h_topic  = topic
    
        
        if type(author) is type or len(indice['author'][h_author])==0:
            ts = indice['topic'][h_topic]
        elif type(topic) is type or len(indice['topic'][h_topic])==0:
            ts = indice['author'][h_author]
    
        #verifica se mais autores participararam desse topico do que esse autor participou de topicos, de modo a otimizar a busca indexada
        elif(len(indice['author'][h_author]) < len(indice['topic'][h_topic])):
            ts = indice['author'][h_author]
        else:
            ts = indice['topic'][h_topic]
        
        return ts
    
    def validate_user(self,t,passwd):
        indice = self.tuplespace[len(t)]
        author = t[0]#hash(t[0])
        if author not in indice['passwd'].keys():
            print('O usuário não possui uma senha associada')
            return False
        elif self.verify_password(indice['passwd'][author],passwd) == False:
            print('A senha está incorreta.')
            return False
        return True
    
    #l = lista de tuplas para realizar a busca
    #a = atributo posicional da tupla para comparação
    #v = valor de comparação
    #i = se deseja inserir ou não (caso i == True é sempre devolvido a posição onde v deveria estar em l)
    def binary_search(self, l, a, v, i=False):
        if len(l) is 0:
            return 0
        low = 0
        high = len(l)-1
        while low <= high: 
            mid = (low+high)//2
            if l[mid][a] > v: high = mid-1
            elif l[mid][a] < v: low = mid+1
            else: return mid
        if i==True:
            return mid
        else:
            return -1

    
    def rdp(self,t):
        ts = self.validate_args(t)
        if ts == False:
            return False
        return self.find(t, ts)

    def remove_all(self, t):
        indice = self.tuplespace[len(t)]
        #era hash antes
        ts = indice['author'][t[0]][t[1]]
        #print('autor',indice['author'][t[0]][t[1]])
        #print('topico',indice['topic'][t[1]][t[0]])
        ts.remove(t)
        #print('autor',indice['author'][t[0]][t[1]])
        #print('topico',indice['topic'][t[1]][t[0]])

    def find(self, t, ts, remove=False, passwd=''):
        for key in ts:
            match = 1
            #print('chave:', key)
            #print('teesse:',ts[key])
            for item in ts[key]:
                #compara os elementos da sua Query com os Elementos do tuplespace
                #print('comparacao',item, t)
                match = 1
                for q,e in zip(t,item):
                    #print('query:',q,'elemtent:',e)
                    if type(q) == type:
                        if q != object and q != type(e):
                            print('não deu match de tipo')
                            match = 0
                            break
                    elif q != e:
                        match = 0
                        break
                
                if match==1:    #remove todas as menções à tupla, e retorna essa tupla
                    #print('chave:', key)
                    #print('teesse:',item)
                    ret = item
                    if remove:
                        if self.validate_user(item,passwd) == False:
                            return False
                        #print(ts[key])
                        
                        #ts[key].remove(item)   #da no mesmo que a função
                        self.remove_all(ret)
                        
                    #print(ret)
                    #print(ts[key])
                    return ret
        return False


    def inp(self,t,passwd):
        ts = self.validate_args(t)
    
        if ts == False:
            return False
        
        return self.find(t, ts, True, passwd)   


if __name__ == '__main__':
    lnd = lindatp()
    
    senhaa = 'penha'
    senhab = '100a'
    b = ('borg','ahoy',3, 0, 0)
    bb = ('blig','ahoy','aaa', 0 , 0)
    d = ('blop','ayo',990, 0, 0)
    e = ('prope','ayo',99, 0, 0)
    a = (2,2,5, 0, 0)
    c = (object, 'assunto', object, object, object)
    print('a: ',a)
    print('b: ',b)
    print('c: ',c)
    print('d: ',d)
    print('e: ',e)
    print(b[1])
    lnd.outp(a,senhaa)
    lnd.outp(b,senhab)
    lnd.outp(bb,senhab)
    lnd.outp(d,'senha')
    lnd.outp(e,'eeeee')
    print('procura b')
    print('achou:',lnd.rdp(b))
    print('procura c')
    print('achou:',lnd.rdp(c))
    #print('inp1: ', lnd.inp(b,senhab))
    print('rdp1: ', lnd.rdp(b))
    #print('inp2: ', lnd.inp(c,senhab))
    #print('inp3: ', lnd.inp(c,senhab))
    b = b + (9,0)
    print(b)
    print(lnd.tuplespace)

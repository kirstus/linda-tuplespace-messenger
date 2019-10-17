import hashlib, binascii, os, time


# tuple = (autor, topico, msg, [ ... ,]* time_sent, msg_number)
class lindatp():
    tuplespace = {}
    
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
        
        #t = t + (1,2)
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
    
        author = hash(author)
        topic = hash(topic)
        print('hashes: ', author, topic)
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
        print(indice['author'][author][topic])
        #indice['topic'][topic][author].append(t[0:-2]+(timenow,1))
        print(indice['topic'][topic][author])
        print(self.tuplespace[len(t)])
    
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
    
        h_author = hash(author)
        h_topic  = hash(topic)
    
        
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
        print(len(t))
        indice = self.tuplespace[len(t)]
        author = hash(t[0])
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
        #try{
        ts = indice['author'][hash(t[0])][hash(t[1])]
        print('autor',indice['author'][hash(t[0])][hash(t[1])])
        print('topico',indice['topic'][hash(t[1])][hash(t[0])])
        ts.remove(t)
        print('autor',indice['author'][hash(t[0])][hash(t[1])])
        print('topico',indice['topic'][hash(t[1])][hash(t[0])])

    def find(self, t, ts, remove=False, passwd=''):
        for key in ts:
            match = 1
            #print('chave:', key)
            #print('teesse:',ts[key])
            for item in ts[key]:
                #compara os elementos da sua Query com os Elementos do tuplespace
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
                        print('chave:', key)
                        print('teesse:',item)
                        ret = item
                        if remove:
                            if self.validate_user(item,passwd) == False:
                                return False
                            print(ts[key])
                        
                            #ts[key].remove(item)   #da no mesmo que a função
                            self.remove_all(ret)
                        
                        print(ret)
                        print(ts[key])
                        return ret
        return False


    def inp(self,t,passwd):
        ts = self.validate_args(t)
    
        if ts == False:
            return False
        print(ts)
        
        return self.find(t, ts, True, passwd)   

#### FALTA
# ordenar as listas por meio desses numeros de mensagem
# fazer busca binaria para encontrar as tuplas a serem eliminadas


if __name__ == '__main__':
    lnd = lindatp()
    
    senhaa = 'senha a'
    senhab = 'koolpass'
    b = ('claudinho','assunto',3, 0, 0)
    bb = ('claudinho','assunto','opora', 0 , 0)
    d = ('bochecha','assunto',990, 0, 0)
    e = ('claudinho','topico',99, 0, 0)
    a = (2,2,5, 0, 0)
    c = (object, 'assunto', object, object, object)
    print('a: ',a)
    print('b: ',b)
    print('c: ',c)
    print('d: ',d)
    print(b[1])
    lnd.outp(a,senhaa)
    lnd.outp(b,senhab)
    lnd.outp(bb,senhab)
    lnd.outp(d,'senha')
    print('procura b')
    print('achou:',lnd.rdp(b))
    print('procura c')
    print('achou:',lnd.rdp(c))
    print('inp1: ', lnd.inp(b,senhab))
    print('rdp1: ', lnd.rdp(b))
    print('inp2: ', lnd.inp(c,senhab))
    print('inp3: ', lnd.inp(c,senhab))
    b = b + (9,0)
    print(b)
